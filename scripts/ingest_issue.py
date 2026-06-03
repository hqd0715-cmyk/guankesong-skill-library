import argparse
import hashlib
import json
import re
import unicodedata
from datetime import date
from pathlib import Path


CATEGORY_DIRS = {
    "AI Shock": "ai-shock",
    "AI + 专业方法论": "ai-professional",
    "整活 Skill": "fun-skills",
    "库维护工具": "library-tools",
}

FIELD_ALIASES = {
    "Skill 标题": "title",
    "Skill 英文 ID": "name",
    "分类": "category",
    "作者": "author",
    "GitHub 用户名": "github",
    "标签": "tags",
    "难度": "difficulty",
    "适用场景": "scenario",
    "使用步骤": "steps",
    "Prompt 示例": "prompt",
    "注意事项": "notes",
    "案例": "example",
}


def normalize_text(value: str) -> str:
    return unicodedata.normalize("NFKC", value or "").strip()


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "")
    value = value.encode("ascii", "ignore").decode("ascii").lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value[:63].strip("-")


def remove_reserved_terms(value: str) -> str:
    parts = [part for part in value.split("-") if part not in {"anthropic", "claude"}]
    return "-".join(parts).strip("-")


def skill_name(title: str, tags: list[str], issue_number: str | None) -> str:
    for candidate in [title, " ".join(tags[:3])]:
        slug = remove_reserved_terms(slugify(candidate))
        if slug:
            return slug

    seed = "|".join([title, ",".join(tags), issue_number or ""])
    digest = hashlib.sha1(seed.encode("utf-8")).hexdigest()[:8]
    return f"skill-{digest}"


def parse_issue_form(body: str) -> dict:
    fields = {}
    current = None
    chunks = []

    for line in body.splitlines():
        heading = re.match(r"^###\s+(.+?)\s*$", line)
        if heading:
            if current:
                fields[current] = "\n".join(chunks).strip()
            label = heading.group(1).strip()
            current = FIELD_ALIASES.get(label)
            chunks = []
            continue
        if current:
            chunks.append(line)

    if current:
        fields[current] = "\n".join(chunks).strip()

    return fields


def clean_value(value: str) -> str:
    value = normalize_text(value)
    if value == "_No response_":
        return ""
    return value


def yaml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def split_tags(raw: str) -> list[str]:
    parts = re.split(r"[,，、\n]+", raw or "")
    return [part.strip() for part in parts if part.strip()]


def first_sentence(value: str, fallback: str) -> str:
    value = re.sub(r"\s+", " ", clean_value(value))
    if not value:
        return fallback
    return value[:120].rstrip()


def description_for(fields: dict) -> str:
    title = clean_value(fields.get("title", "未命名 Skill")) or "未命名 Skill"
    scenario = first_sentence(fields.get("scenario", ""), "需要复用该投稿中的工作流、步骤或 Prompt 时")
    tags = split_tags(clean_value(fields.get("tags", "")))
    tag_text = f"关键词：{', '.join(tags[:5])}。" if tags else ""
    return f"{title}。用于{scenario}。{tag_text}Use when the user asks for this workflow, prompt pattern, or reusable AI skill."


def skill_markdown(skill_id: str, fields: dict) -> str:
    title = clean_value(fields.get("title", "未命名 Skill")) or "未命名 Skill"
    frontmatter = [
        "---",
        f"name: {yaml_quote(skill_id)}",
        f"description: {yaml_quote(description_for(fields))}",
        "---",
    ]

    sections = [
        f"# {title}",
        "## 适用场景",
        clean_value(fields.get("scenario", "")) or "待补充。",
        "## 使用步骤",
        clean_value(fields.get("steps", "")) or "待补充。",
        "## Prompt 示例",
        clean_value(fields.get("prompt", "")) or "待补充。",
        "## 注意事项",
        clean_value(fields.get("notes", "")) or "无。",
        "## 案例",
        clean_value(fields.get("example", "")) or "待补充。",
    ]

    return "\n".join(frontmatter) + "\n\n" + "\n\n".join(sections) + "\n"


def metadata_json(skill_id: str, fields: dict, issue_number: str | None) -> dict:
    today = date.today().isoformat()
    category = clean_value(fields.get("category", "AI Shock")) or "AI Shock"
    if category not in CATEGORY_DIRS:
        category = "AI Shock"

    data = {
        "name": skill_id,
        "title": clean_value(fields.get("title", "未命名 Skill")) or "未命名 Skill",
        "category": category,
        "author": clean_value(fields.get("author", "")),
        "github": clean_value(fields.get("github", "")),
        "tags": split_tags(clean_value(fields.get("tags", ""))),
        "status": "draft",
        "created": today,
        "updated": today,
        "difficulty": clean_value(fields.get("difficulty", "beginner")) or "beginner",
        "platforms": ["codex", "claude-code"],
    }
    if issue_number:
        data["source_issue"] = int(issue_number) if issue_number.isdigit() else issue_number
    return data


def parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}

    data = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        try:
            data[key.strip()] = json.loads(value)
        except json.JSONDecodeError:
            data[key.strip()] = value.strip('"')
    return data


def first_heading(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.parent.name


def read_metadata(skill_dir: Path) -> dict:
    path = skill_dir / "skill.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_skill_package(root: Path, fields: dict, issue_number: str | None) -> Path:
    title = clean_value(fields.get("title", "未命名 Skill")) or "未命名 Skill"
    tags = split_tags(clean_value(fields.get("tags", "")))
    explicit_name = slugify(clean_value(fields.get("name", "")))
    skill_id = explicit_name or skill_name(title, tags, issue_number)
    category = clean_value(fields.get("category", "AI Shock")) or "AI Shock"
    category_dir = CATEGORY_DIRS.get(category, "ai-shock")
    target = root / "skills" / category_dir / skill_id
    target.mkdir(parents=True, exist_ok=True)
    (target / "SKILL.md").write_text(skill_markdown(skill_id, fields), encoding="utf-8")
    (target / "skill.json").write_text(
        json.dumps(metadata_json(skill_id, fields, issue_number), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return target


def rebuild_index(root: Path) -> None:
    skills = []
    for skill_file in sorted((root / "skills").glob("*/*/SKILL.md")):
        frontmatter = parse_frontmatter(skill_file)
        metadata = read_metadata(skill_file.parent)
        name = frontmatter.get("name") or metadata.get("name") or skill_file.parent.name
        metadata_path = skill_file.parent / "skill.json"
        skills.append(
            {
                "name": name,
                "title": metadata.get("title") or first_heading(skill_file),
                "description": frontmatter.get("description", ""),
                "category": metadata.get("category", ""),
                "author": metadata.get("author", ""),
                "github": metadata.get("github", ""),
                "tags": metadata.get("tags", []),
                "difficulty": metadata.get("difficulty", ""),
                "status": metadata.get("status", ""),
                "platforms": metadata.get("platforms", []),
                "path": skill_file.relative_to(root).as_posix(),
                "metadata_path": metadata_path.relative_to(root).as_posix() if metadata_path.exists() else "",
            }
        )

    index_dir = root / "index"
    index_dir.mkdir(exist_ok=True)
    (index_dir / "skills.json").write_text(
        json.dumps(skills, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--issue-number")
    parser.add_argument("--issue-title")
    parser.add_argument("--issue-body-file")
    parser.add_argument("--rebuild-index", action="store_true")
    args = parser.parse_args()

    root = Path.cwd()
    if args.rebuild_index:
        rebuild_index(root)
        return

    if not args.issue_body_file:
        raise SystemExit("--issue-body-file is required unless --rebuild-index is used")

    body = Path(args.issue_body_file).read_text(encoding="utf-8")
    fields = {key: clean_value(value) for key, value in parse_issue_form(body).items()}
    if args.issue_title and not fields.get("title"):
        fields["title"] = re.sub(r"^\[Skill\]\s*", "", args.issue_title).strip()

    write_skill_package(root, fields, args.issue_number)
    rebuild_index(root)


if __name__ == "__main__":
    main()
