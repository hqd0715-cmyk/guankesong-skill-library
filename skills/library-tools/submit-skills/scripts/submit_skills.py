import argparse
import json
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

CATEGORY_DIRS = {
    "AI Shock": "ai-shock",
    "AI + 专业方法论": "ai-professional",
    "整活 Skill": "fun-skills",
    "库维护工具": "library-tools",
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


def current_github_user(repo_dir: Path) -> dict:
    if not shutil.which("gh"):
        return {}

    try:
        result = subprocess.run(
            ["gh", "api", "user", "--jq", "{login:.login,name:.name}"],
            cwd=repo_dir,
            text=True,
            capture_output=True,
        )
    except FileNotFoundError:
        return {}

    if result.returncode != 0:
        return {}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {}


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


def read_metadata(skill_dir: Path) -> dict:
    metadata_file = skill_dir / "skill.json"
    if not metadata_file.exists():
        return {}
    return json.loads(metadata_file.read_text(encoding="utf-8"))


def write_metadata(skill_dir: Path, metadata: dict) -> None:
    metadata_file = skill_dir / "skill.json"
    metadata_file.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def apply_contributor(metadata: dict, author: str | None, github: str | None, gh_user: dict) -> dict:
    updated = dict(metadata)
    if author:
        updated["author"] = author
    elif not str(updated.get("author", "")).strip() and gh_user.get("name"):
        updated["author"] = gh_user["name"]
    elif not str(updated.get("author", "")).strip() and gh_user.get("login"):
        updated["author"] = gh_user["login"]

    github_login = github or gh_user.get("login")
    if github_login:
        updated["github"] = github_login.lstrip("@")
    return updated


def ensure_contributor(metadata: dict, skill_dir: Path) -> None:
    if not str(metadata.get("author", "")).strip():
        raise SystemExit(
            f"{skill_dir}: missing contributor author. Add skill.json author or pass --author."
        )


def category_dir_for(metadata: dict, skill_dir: Path) -> str:
    category = str(metadata.get("category", "AI Shock") or "AI Shock").strip()
    if category not in CATEGORY_DIRS:
        supported = ", ".join(CATEGORY_DIRS)
        raise SystemExit(
            f"{skill_dir}: unsupported category '{category}'. Supported categories: {supported}."
        )
    return CATEGORY_DIRS[category]


def prepare_skill_metadata(
    skill_dir: Path,
    author: str | None,
    github: str | None,
    gh_user: dict,
) -> dict:
    metadata = apply_contributor(read_metadata(skill_dir), author, github, gh_user)
    ensure_contributor(metadata, skill_dir)
    return metadata


def ensure_clean_repo(repo_dir: Path, allow_dirty: bool) -> None:
    status = run(["git", "status", "--porcelain"], cwd=repo_dir).stdout.strip()
    if status and not allow_dirty:
        raise SystemExit(
            "Repository has uncommitted changes. Commit/stash them first, or rerun with --allow-dirty."
        )


def relative_to_repo(repo_dir: Path, path: Path) -> str:
    return path.resolve().relative_to(repo_dir.resolve()).as_posix()


def skill_name_for(skill_dir: Path) -> str:
    frontmatter = parse_frontmatter(skill_dir / "SKILL.md")
    name = frontmatter.get("name", "").strip()
    if not name:
        raise SystemExit(f"{skill_dir}: SKILL.md frontmatter must include name")
    return name


def target_for_skill(skill_dir: Path, repo_dir: Path, metadata: dict) -> Path:
    name = skill_name_for(skill_dir)
    target = repo_dir / "skills" / category_dir_for(metadata, skill_dir) / name
    target_parent = (repo_dir / "skills").resolve()
    resolved_target = target.resolve()
    if target_parent not in [resolved_target, *resolved_target.parents]:
        raise SystemExit(f"Refusing to write outside skills/: {target}")
    return target


def conflicting_skill_paths(repo_dir: Path, name: str, target: Path) -> list[Path]:
    return [
        existing
        for existing in (repo_dir / "skills").glob(f"*/{name}")
        if existing.resolve() != target.resolve()
    ]


def ensure_no_unapproved_conflicts(
    skill_dir: Path,
    repo_dir: Path,
    name: str,
    conflicts: list[Path],
    replace_existing: bool,
) -> None:
    if conflicts and not replace_existing:
        conflict_list = ", ".join(relative_to_repo(repo_dir, path) for path in conflicts)
        raise SystemExit(
            f"{skill_dir}: skill name '{name}' already exists in another category: {conflict_list}. "
            "Rerun with --replace-existing to move it."
        )


def copy_skill(
    skill_dir: Path,
    repo_dir: Path,
    metadata: dict,
    replace_existing: bool,
) -> list[Path]:
    name = skill_name_for(skill_dir)
    target = target_for_skill(skill_dir, repo_dir, metadata)

    changed_paths = [target]
    existing_conflicts = conflicting_skill_paths(repo_dir, name, target)
    ensure_no_unapproved_conflicts(skill_dir, repo_dir, name, existing_conflicts, replace_existing)

    if skill_dir.resolve() == target.resolve():
        write_metadata(target, metadata)
        print(f"Already in target location: {target.relative_to(repo_dir)}")
        return changed_paths

    for existing in existing_conflicts:
        shutil.rmtree(existing)
        changed_paths.append(existing)

    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(skill_dir, target, ignore=should_ignore)
    write_metadata(target, metadata)
    print(f"Copied {skill_dir} -> {target.relative_to(repo_dir)}")
    return changed_paths


def rebuild_and_validate(repo_dir: Path) -> None:
    run([sys.executable, "scripts/ingest_issue.py", "--rebuild-index"], cwd=repo_dir)
    run([sys.executable, "scripts/validate_skills.py"], cwd=repo_dir)


def commit_changes(repo_dir: Path, branch: str, message: str, paths: list[Path]) -> bool:
    run(["git", "checkout", "-B", branch], cwd=repo_dir)

    add_paths = []
    seen = set()
    for path in [*paths, repo_dir / "index" / "skills.json"]:
        relative_path = relative_to_repo(repo_dir, path)
        if relative_path not in seen:
            seen.add(relative_path)
            add_paths.append(relative_path)
    run(["git", "add", "--", *add_paths], cwd=repo_dir)

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
    parser.add_argument("--message", default=f"{datetime.now():%Y-%m-%d %H:%M}～提交本地 Skill 到共创库审核")
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--base", default="main")
    parser.add_argument("--author", help="Contributor display name. Defaults to GitHub profile name/login if missing.")
    parser.add_argument("--github", help="Contributor GitHub username. Defaults to the current gh login when available.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--push", action="store_true")
    parser.add_argument("--create-pr", action="store_true")
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument(
        "--replace-existing",
        action="store_true",
        help="Move a skill when the same name already exists in another category.",
    )
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

    gh_user = current_github_user(repo_dir) if not args.author or not args.github else {}
    planned_skills = []
    print("Detected skill packages:")
    for skill_dir in skill_dirs:
        name = skill_name_for(skill_dir)
        metadata = prepare_skill_metadata(skill_dir, args.author, args.github, gh_user)
        target = target_for_skill(skill_dir, repo_dir, metadata)
        conflicts = conflicting_skill_paths(repo_dir, name, target)
        ensure_no_unapproved_conflicts(skill_dir, repo_dir, name, conflicts, args.replace_existing)
        planned_skills.append((skill_dir, metadata))
        contributor = metadata.get("author", "")
        github = metadata.get("github", "")
        suffix = f" by {contributor}" + (f" (@{github})" if github else "")
        print(f"- {name} from {skill_dir}{suffix} -> {relative_to_repo(repo_dir, target)}")

    if args.dry_run:
        return 0

    ensure_clean_repo(repo_dir, args.allow_dirty)
    copied_paths = []
    for skill_dir, metadata in planned_skills:
        copied_paths.extend(copy_skill(skill_dir, repo_dir, metadata, args.replace_existing))
    rebuild_and_validate(repo_dir)
    committed = commit_changes(repo_dir, args.branch, args.message, copied_paths)

    if committed and args.push:
        run(["git", "push", "-u", args.remote, args.branch], cwd=repo_dir)
        if args.create_pr:
            if not shutil.which("gh"):
                raise SystemExit("--create-pr requires GitHub CLI (gh). Push completed; create the PR manually.")
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
                    f"内部代投稿 Skill：{args.branch}",
                    "--body",
                    "由莞客松内部整理人使用 submit-skills 代为提交，等待维护者审核来源、署名、公开状态和 Skill 质量。",
                ],
                cwd=repo_dir,
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
