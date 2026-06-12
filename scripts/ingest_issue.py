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

VALID_SKILL_NAME = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
RESERVED_NAME_PARTS = {"anthropic", "claude"}
VALID_DIFFICULTIES = {"beginner", "intermediate", "advanced"}
VALID_PUBLICATION_STATUSES = {"已确认适合公开", "需进一步核查"}
VALID_SUBMISSION_TYPES = {
    "internal-proxy",
    "external-claude-code",
    "external-codex",
    "external-manual",
}
CORE_FIELDS = {
    "title": "Skill 标题",
    "category": "分类",
    "author": "作者 / 公开署名",
    "scenario": "适用场景",
    "steps": "使用步骤",
}

FIELD_ALIASES = {
    "Skill 标题": "title",
    "标题": "title",
    "Skill 英文 ID": "name",
    "英文 ID": "name",
    "英文ID": "name",
    "Skill ID": "name",
    "分类": "category",
    "作者": "author",
    "作者 / 公开署名": "author",
    "作者/公开署名": "author",
    "原始提供者": "source_provider",
    "素材提供者": "source_provider",
    "提供者": "source_provider",
    "素材来源": "source",
    "来源": "source",
    "整理人": "curator",
    "整理负责人": "curator",
    "GitHub 用户名": "github",
    "GitHub用户名": "github",
    "标签": "tags",
    "难度": "difficulty",
    "适用场景": "scenario",
    "使用步骤": "steps",
    "Prompt 示例": "prompt",
    "提示词示例": "prompt",
    "Prompt": "prompt",
    "提示词": "prompt",
    "注意事项": "notes",
    "案例": "example",
    "公开状态": "publication_status",
    "是否适合公开": "publication_status",
    "投稿方式": "submission_type",
    "提交方式": "submission_type",
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
    parts = [part for part in value.split("-") if part not in RESERVED_NAME_PARTS]
    return "-".join(parts).strip("-")


def skill_name(title: str, tags: list[str], issue_number: str | None) -> str:
    for candidate in [title, " ".join(tags[:3])]:
        slug = remove_reserved_terms(slugify(candidate))
        if slug:
            return slug

    seed = "|".join([title, ",".join(tags), issue_number or ""])
    digest = hashlib.sha1(seed.encode("utf-8")).hexdigest()[:8]
    return f"skill-{digest}"


def normalize_category(value: str) -> str:
    normalized = clean_value(value)
    aliases = {
        "ai shock": "AI Shock",
        "ai-shock": "AI Shock",
        "ai + 专业方法论": "AI + 专业方法论",
        "ai-professional": "AI + 专业方法论",
        "整活 skill": "整活 Skill",
        "fun-skills": "整活 Skill",
        "库维护工具": "库维护工具",
        "library-tools": "库维护工具",
    }
    category = aliases.get(normalized.lower(), normalized)
    if category not in CATEGORY_DIRS:
        supported = ", ".join(CATEGORY_DIRS)
        raise ValueError(f"不支持的分类“{value}”。可选值：{supported}")
    return category


def validate_explicit_skill_name(value: str) -> str:
    name = clean_value(value)
    if not VALID_SKILL_NAME.fullmatch(name):
        raise ValueError(
            "Skill 英文 ID 只能包含小写字母、数字和连字符，长度不超过 64，且首尾必须是字母或数字"
        )
    reserved = RESERVED_NAME_PARTS & set(name.split("-"))
    if reserved:
        raise ValueError("Skill 英文 ID 不能包含保留词：anthropic、claude")
    return name


def normalize_submission_type(value: str) -> str:
    submission_type = clean_value(value) or "internal-proxy"
    if submission_type not in VALID_SUBMISSION_TYPES:
        supported = ", ".join(sorted(VALID_SUBMISSION_TYPES))
        raise ValueError(f"不支持的投稿方式“{submission_type}”。可选值：{supported}")
    return submission_type


def validate_submission_fields(fields: dict) -> dict:
    normalized = {key: clean_value(value) for key, value in fields.items()}
    missing = [label for key, label in CORE_FIELDS.items() if not normalized.get(key)]
    if missing:
        raise ValueError(f"缺少必填字段：{', '.join(missing)}")

    normalized["category"] = normalize_category(normalized["category"])
    normalized["submission_type"] = normalize_submission_type(
        normalized.get("submission_type", "")
    )
    if normalized.get("name"):
        normalized["name"] = validate_explicit_skill_name(normalized["name"])

    difficulty = normalized.get("difficulty", "") or "beginner"
    if difficulty not in VALID_DIFFICULTIES:
        raise ValueError(
            f"不支持的难度“{difficulty}”。可选值：{', '.join(sorted(VALID_DIFFICULTIES))}"
        )
    normalized["difficulty"] = difficulty

    publication_status = normalized.get("publication_status", "") or "需进一步核查"
    if publication_status not in VALID_PUBLICATION_STATUSES:
        raise ValueError(
            f"不支持的公开状态“{publication_status}”。"
            f"可选值：{', '.join(sorted(VALID_PUBLICATION_STATUSES))}"
        )
    normalized["publication_status"] = publication_status
    return normalized


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


def metadata_json(
    skill_id: str,
    fields: dict,
    issue_number: str | None,
    issue_author: str | None = None,
) -> dict:
    today = date.today().isoformat()
    category = normalize_category(fields.get("category", "AI Shock"))
    submission_type = normalize_submission_type(fields.get("submission_type", ""))
    submitted_github = clean_value(fields.get("github", ""))
    if submission_type.startswith("external-"):
        github = clean_value(issue_author or "")
    else:
        github = submitted_github or clean_value(issue_author or "")

    data = {
        "name": skill_id,
        "title": clean_value(fields.get("title", "未命名 Skill")) or "未命名 Skill",
        "category": category,
        "author": clean_value(fields.get("author", "")),
        "source_provider": clean_value(fields.get("source_provider", "")),
        "source": clean_value(fields.get("source", "")),
        "curator": clean_value(fields.get("curator", "")),
        "github": github,
        "tags": split_tags(clean_value(fields.get("tags", ""))),
        "status": "draft",
        "created": today,
        "updated": today,
        "difficulty": clean_value(fields.get("difficulty", "beginner")) or "beginner",
        "platforms": ["codex", "claude-code"],
        "publication_status": clean_value(fields.get("publication_status", ""))
        or "需进一步核查",
        "submission_type": submission_type,
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


def unique_target(
    root: Path,
    category_dir: str,
    skill_id: str,
    issue_number: str | None,
) -> tuple[str, Path]:
    target = root / "skills" / category_dir / skill_id
    if not target.exists():
        return skill_id, target

    metadata = read_metadata(target)
    if (
        issue_number
        and str(metadata.get("source_issue", "")) == str(issue_number)
        and metadata.get("status", "draft") == "draft"
    ):
        return skill_id, target

    if not issue_number:
        raise ValueError(f"Skill 目录已存在，拒绝覆盖：{target}")

    suffix = f"-issue-{issue_number}"
    candidate = f"{skill_id[: 63 - len(suffix)].rstrip('-')}{suffix}"
    alternative = root / "skills" / category_dir / candidate
    if alternative.exists():
        raise ValueError(f"Skill 目录及 Issue 备用目录均已存在，拒绝覆盖：{alternative}")
    return candidate, alternative


def write_skill_package(
    root: Path,
    fields: dict,
    issue_number: str | None,
    issue_author: str | None = None,
) -> Path:
    fields = validate_submission_fields(fields)
    title = fields["title"]
    tags = split_tags(clean_value(fields.get("tags", "")))
    explicit_name = fields.get("name", "")
    skill_id = explicit_name or skill_name(title, tags, issue_number)
    category_dir = CATEGORY_DIRS[fields["category"]]
    skill_id, target = unique_target(root, category_dir, skill_id, issue_number)
    target.mkdir(parents=True, exist_ok=True)
    (target / "SKILL.md").write_text(skill_markdown(skill_id, fields), encoding="utf-8")
    (target / "skill.json").write_text(
        json.dumps(
            metadata_json(skill_id, fields, issue_number, issue_author),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
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
    parser.add_argument("--issue-title-file")
    parser.add_argument("--issue-author")
    parser.add_argument("--issue-body-file")
    parser.add_argument("--print-field", choices=sorted(set(FIELD_ALIASES.values())))
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
    issue_title = args.issue_title
    if args.issue_title_file:
        issue_title = Path(args.issue_title_file).read_text(encoding="utf-8").strip()
    if issue_title and not fields.get("title"):
        fields["title"] = re.sub(r"^\[Skill\]\s*", "", issue_title).strip()

    if args.print_field:
        if args.print_field == "submission_type":
            print(normalize_submission_type(fields.get(args.print_field, "")))
        else:
            print(fields.get(args.print_field, ""))
        return

    try:
        write_skill_package(root, fields, args.issue_number, args.issue_author)
    except ValueError as exc:
        raise SystemExit(f"Issue 投稿内容无效：{exc}") from exc
    rebuild_index(root)


if __name__ == "__main__":
    main()
