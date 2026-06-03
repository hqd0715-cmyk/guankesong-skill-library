import json
import re
import sys
from pathlib import Path


VALID_NAME = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
VALID_FRONTMATTER_KEYS = {"name", "description"}
VALID_CATEGORY_DIRS = {
    "AI Shock": "ai-shock",
    "AI + 专业方法论": "ai-professional",
    "整活 Skill": "fun-skills",
    "库维护工具": "library-tools",
}
VALID_CATEGORIES = {*VALID_CATEGORY_DIRS, ""}
RESERVED_NAME_PARTS = {"anthropic", "claude"}


def parse_frontmatter(path: Path) -> tuple[dict, set[str]]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("frontmatter is not closed")

    data = {}
    keys = set()
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        key = key.strip()
        keys.add(key)
        value = value.strip()
        try:
            data[key] = json.loads(value)
        except json.JSONDecodeError:
            data[key] = value.strip('"')
    return data, keys


def validate_skill(skill_dir: Path, skills_root: Path) -> list[str]:
    errors = []
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        return [f"{skill_dir}: missing SKILL.md"]

    try:
        frontmatter, keys = parse_frontmatter(skill_file)
    except ValueError as exc:
        return [f"{skill_file}: {exc}"]

    extra_keys = keys - VALID_FRONTMATTER_KEYS
    missing_keys = VALID_FRONTMATTER_KEYS - keys
    if extra_keys:
        errors.append(f"{skill_file}: unsupported frontmatter keys: {', '.join(sorted(extra_keys))}")
    if missing_keys:
        errors.append(f"{skill_file}: missing frontmatter keys: {', '.join(sorted(missing_keys))}")

    name = str(frontmatter.get("name", ""))
    description = str(frontmatter.get("description", ""))
    if not VALID_NAME.match(name):
        errors.append(f"{skill_file}: invalid skill name '{name}'")
    if RESERVED_NAME_PARTS & set(name.split("-")):
        errors.append(f"{skill_file}: name must not contain reserved terms: anthropic, claude")
    if name != skill_dir.name:
        errors.append(f"{skill_file}: frontmatter name must match folder '{skill_dir.name}'")
    if skill_dir.parent.parent != skills_root:
        errors.append(f"{skill_file}: skill package must live under skills/<category>/<name>/")
    if len(description.strip()) < 20:
        errors.append(f"{skill_file}: description is too short")

    metadata_file = skill_dir / "skill.json"
    if metadata_file.exists():
        try:
            metadata = json.loads(metadata_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{metadata_file}: invalid JSON: {exc}")
            metadata = {}
        if metadata.get("name") and metadata.get("name") != name:
            errors.append(f"{metadata_file}: name must match SKILL.md")
        if metadata.get("category", "") not in VALID_CATEGORIES:
            errors.append(f"{metadata_file}: unsupported category '{metadata.get('category')}'")
        expected_category_dir = VALID_CATEGORY_DIRS.get(metadata.get("category", ""))
        if expected_category_dir and skill_dir.parent.name != expected_category_dir:
            errors.append(
                f"{metadata_file}: category '{metadata.get('category')}' must live under skills/{expected_category_dir}/"
            )
        if not isinstance(metadata.get("tags", []), list):
            errors.append(f"{metadata_file}: tags must be a list")
        if "platforms" in metadata and not isinstance(metadata["platforms"], list):
            errors.append(f"{metadata_file}: platforms must be a list")

    return errors


def main() -> int:
    root = Path.cwd()
    skills_root = root / "skills"
    if not skills_root.exists():
        print("skills directory not found", file=sys.stderr)
        return 1

    skill_dirs = sorted(path for path in skills_root.glob("*/*") if path.is_dir() and (path / "SKILL.md").exists())
    errors = []
    for skill_dir in skill_dirs:
        errors.extend(validate_skill(skill_dir, skills_root))

    if not skill_dirs:
        errors.append("no skill packages found under skills/<category>/<name>/SKILL.md")

    direct_skill_files = sorted(skills_root.glob("*/SKILL.md"))
    for skill_file in direct_skill_files:
        errors.append(f"{skill_file}: direct skills are not allowed; use skills/<category>/<name>/SKILL.md")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(skill_dirs)} skill packages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
