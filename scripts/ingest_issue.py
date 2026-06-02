import argparse
import json
import re
import unicodedata
from datetime import date
from pathlib import Path


CATEGORY_DIRS = {
    "AI Shock": "ai-shock",
    "AI + 专业方法论": "ai-professional",
    "整活 Skill": "fun-skills",
}

FIELD_ALIASES = {
    "Skill 标题": "title",
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


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).strip().lower()
    value = re.sub(r"[^\w\u4e00-\u9fff]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "untitled"


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
    value = value.strip()
    if value == "_No response_":
        return ""
    return value


def yaml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def split_tags(raw: str) -> list[str]:
    parts = re.split(r"[,，、\n]+", raw or "")
    return [part.strip() for part in parts if part.strip()]


def skill_markdown(fields: dict, issue_number: str | None) -> str:
    today = date.today().isoformat()
    title = clean_value(fields.get("title", "未命名 Skill"))
    category = clean_value(fields.get("category", "AI Shock"))
    author = clean_value(fields.get("author", ""))
    github = clean_value(fields.get("github", ""))
    difficulty = clean_value(fields.get("difficulty", "beginner"))
    tags = split_tags(clean_value(fields.get("tags", "")))

    frontmatter = [
        "---",
        f"title: {yaml_quote(title)}",
        f"category: {yaml_quote(category)}",
        f"author: {yaml_quote(author)}",
        f"github: {yaml_quote(github)}",
        f"tags: {json.dumps(tags, ensure_ascii=False)}",
        'status: "draft"',
        f'created: "{today}"',
        f'updated: "{today}"',
        f"difficulty: {yaml_quote(difficulty)}",
        "prerequisites: []",
        "related: []",
    ]
    if issue_number:
        frontmatter.append(f"source_issue: {issue_number}")
    frontmatter.append("---")

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
        value = value.strip().strip('"')
        data[key.strip()] = value
    return data


def rebuild_index(root: Path) -> None:
    skills = []
    for path in sorted((root / "skills").glob("*/*.md")):
        meta = parse_frontmatter(path)
        if not meta:
            continue
        skills.append(
            {
                "title": meta.get("title", path.stem),
                "category": meta.get("category", ""),
                "author": meta.get("author", ""),
                "difficulty": meta.get("difficulty", ""),
                "status": meta.get("status", ""),
                "path": path.relative_to(root).as_posix(),
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

    title = fields.get("title") or "未命名 Skill"
    category = fields.get("category") or "AI Shock"
    category_dir = CATEGORY_DIRS.get(category, "ai-shock")
    slug = slugify(title)
    target = root / "skills" / category_dir / f"{slug}.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(skill_markdown(fields, args.issue_number), encoding="utf-8")
    rebuild_index(root)


if __name__ == "__main__":
    main()
