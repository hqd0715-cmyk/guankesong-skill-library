import argparse
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


EXCLUDED_NAMES = {
    ".git",
    ".DS_Store",
    "Thumbs.db",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
    "templates",
}


def run(command: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    if check and result.returncode != 0:
        raise SystemExit(result.returncode)
    return result


def git_root(path: Path) -> Path | None:
    result = run(["git", "rev-parse", "--show-toplevel"], cwd=path, check=False)
    if result.returncode != 0:
        return None
    return Path(result.stdout.strip()).resolve()


def parse_frontmatter(skill_file: Path) -> dict[str, str]:
    text = skill_file.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{skill_file} missing YAML frontmatter")
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError(f"{skill_file} frontmatter is not closed")

    data = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def find_skill_dirs(source: Path) -> list[Path]:
    source = source.resolve()
    if (source / "SKILL.md").exists():
        return [source]

    skill_dirs = []
    for skill_file in source.rglob("SKILL.md"):
        if any(part in EXCLUDED_NAMES for part in skill_file.parts):
            continue
        skill_dirs.append(skill_file.parent)
    return sorted(set(skill_dirs))


def should_ignore(_directory: str, names: list[str]) -> set[str]:
    return {name for name in names if name in EXCLUDED_NAMES}


def ensure_clean_repo(repo_dir: Path, allow_dirty: bool) -> None:
    status = run(["git", "status", "--porcelain"], cwd=repo_dir).stdout.strip()
    if status and not allow_dirty:
        raise SystemExit(
            "Repository has uncommitted changes. Commit/stash them first, or rerun with --allow-dirty."
        )


def copy_skill(skill_dir: Path, repo_dir: Path) -> Path:
    frontmatter = parse_frontmatter(skill_dir / "SKILL.md")
    name = frontmatter.get("name", "").strip()
    if not name:
        raise SystemExit(f"{skill_dir}: SKILL.md frontmatter must include name")

    target = repo_dir / "skills" / name
    target_parent = (repo_dir / "skills").resolve()
    resolved_target = target.resolve()
    if target_parent not in [resolved_target, *resolved_target.parents]:
        raise SystemExit(f"Refusing to write outside skills/: {target}")

    if skill_dir.resolve() == resolved_target:
        print(f"Already in target location: {target.relative_to(repo_dir)}")
        return target

    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(skill_dir, target, ignore=should_ignore)
    print(f"Copied {skill_dir} -> {target.relative_to(repo_dir)}")
    return target


def rebuild_and_validate(repo_dir: Path) -> None:
    run([sys.executable, "scripts/ingest_issue.py", "--rebuild-index"], cwd=repo_dir)
    run([sys.executable, "scripts/validate_skills.py"], cwd=repo_dir)


def commit_changes(repo_dir: Path, branch: str, message: str, paths: list[Path]) -> bool:
    run(["git", "checkout", "-B", branch], cwd=repo_dir)
    for path in paths:
        run(["git", "add", str(path.relative_to(repo_dir))], cwd=repo_dir)
    run(["git", "add", "index/skills.json"], cwd=repo_dir)

    diff = run(["git", "diff", "--cached", "--stat"], cwd=repo_dir).stdout.strip()
    if not diff:
        print("No changes to commit.")
        return False

    print(diff)
    run(["git", "commit", "-m", message], cwd=repo_dir)
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=".", help="Folder containing one or more Agent Skill packages.")
    parser.add_argument("--repo-dir", help="Local guankesong-skill-library checkout. Defaults to current git root.")
    parser.add_argument("--branch", default=f"skill-submission/local-{datetime.now():%Y%m%d-%H%M}")
    parser.add_argument("--message", default=f"{datetime.now():%Y-%m-%d %H:%M}｜提交本地 Skill 到共创库审核")
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--base", default="main")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--push", action="store_true")
    parser.add_argument("--create-pr", action="store_true")
    parser.add_argument("--allow-dirty", action="store_true")
    args = parser.parse_args()

    source = Path(args.source).resolve()
    repo_dir = Path(args.repo_dir).resolve() if args.repo_dir else git_root(Path.cwd())
    if not repo_dir:
        raise SystemExit("--repo-dir is required when the current directory is not inside a git repository")
    if not (repo_dir / "scripts" / "ingest_issue.py").exists():
        raise SystemExit(f"{repo_dir} does not look like guankesong-skill-library")
    if args.create_pr and not args.push:
        raise SystemExit("--create-pr requires --push")

    skill_dirs = find_skill_dirs(source)
    if not skill_dirs:
        raise SystemExit(f"No SKILL.md files found under {source}")

    print("Detected skill packages:")
    for skill_dir in skill_dirs:
        frontmatter = parse_frontmatter(skill_dir / "SKILL.md")
        print(f"- {frontmatter.get('name', skill_dir.name)} from {skill_dir}")

    if args.dry_run:
        return 0

    ensure_clean_repo(repo_dir, args.allow_dirty)
    copied_paths = [copy_skill(skill_dir, repo_dir) for skill_dir in skill_dirs]
    rebuild_and_validate(repo_dir)
    committed = commit_changes(repo_dir, args.branch, args.message, copied_paths)

    if committed and args.push:
        run(["git", "push", "-u", args.remote, args.branch], cwd=repo_dir)
        if args.create_pr:
            run(
                [
                    "gh",
                    "pr",
                    "create",
                    "--draft",
                    "--base",
                    args.base,
                    "--head",
                    args.branch,
                    "--title",
                    f"投稿 Skill：{args.branch}",
                    "--body",
                    "由 submit-skills 自动整理并提交，等待维护者审核。",
                ],
                cwd=repo_dir,
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
