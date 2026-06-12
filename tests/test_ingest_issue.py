import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
INGEST_PATH = ROOT / "scripts" / "ingest_issue.py"
VALIDATE_PATH = ROOT / "scripts" / "validate_skills.py"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ingest_issue = load_module("ingest_issue", INGEST_PATH)
validate_skills = load_module("validate_skills", VALIDATE_PATH)


def fixture_fields(name):
    body = (FIXTURES / name).read_text(encoding="utf-8")
    return ingest_issue.parse_issue_form(body)


class IssueIngestionTest(unittest.TestCase):
    def test_internal_proxy_fields_are_preserved(self):
        fields = ingest_issue.validate_submission_fields(
            fixture_fields("internal_proxy_issue.md")
        )
        metadata = ingest_issue.metadata_json(
            "event-retrospective", fields, "42", "internal-maintainer"
        )

        self.assertEqual(metadata["author"], "莞客松围炉会共创")
        self.assertEqual(metadata["source_provider"], "围炉会参与者")
        self.assertEqual(metadata["source"], "2026 莞客松围炉会")
        self.assertEqual(metadata["curator"], "莞客松整理组")
        self.assertEqual(metadata["github"], "internal-maintainer")
        self.assertEqual(metadata["submission_type"], "internal-proxy")
        self.assertEqual(metadata["source_issue"], 42)

    def test_external_claude_aliases_and_category_are_normalized(self):
        fields = ingest_issue.validate_submission_fields(
            fixture_fields("external_claude_issue.md")
        )

        self.assertEqual(fields["title"], "会议纪要行动项提取")
        self.assertEqual(fields["name"], "meeting-action-items")
        self.assertEqual(fields["category"], "AI + 专业方法论")
        self.assertEqual(fields["submission_type"], "external-claude-code")
        self.assertEqual(fields["prompt"], "请提取以下会议记录中的行动项。")

    def test_external_codex_generates_stable_name_and_defaults(self):
        fields = ingest_issue.validate_submission_fields(
            fixture_fields("external_codex_issue.md")
        )
        name = ingest_issue.skill_name(
            fields["title"], ingest_issue.split_tags(fields["tags"]), "88"
        )

        self.assertEqual(name, "community-triage-support")
        self.assertEqual(fields["submission_type"], "external-codex")
        self.assertEqual(fields["publication_status"], "需进一步核查")

    def test_external_submission_records_issue_author_not_claimed_account(self):
        fields = ingest_issue.validate_submission_fields(
            fixture_fields("external_claude_issue.md")
        )
        fields["github"] = "someone-else"

        metadata = ingest_issue.metadata_json(
            "meeting-action-items", fields, "52", "actual-issue-author"
        )

        self.assertEqual(metadata["github"], "actual-issue-author")

    def test_missing_core_fields_raise_clear_error(self):
        with self.assertRaisesRegex(
            ValueError, "缺少必填字段：作者 / 公开署名, 适用场景, 使用步骤"
        ):
            ingest_issue.validate_submission_fields(
                {"title": "Incomplete", "category": "AI Shock"}
            )

    def test_invalid_explicit_name_is_not_silently_rewritten(self):
        fields = fixture_fields("internal_proxy_issue.md")
        fields["name"] = "Claude Skill"

        with self.assertRaisesRegex(ValueError, "只能包含小写字母"):
            ingest_issue.validate_submission_fields(fields)

    def test_unknown_category_is_rejected(self):
        fields = fixture_fields("internal_proxy_issue.md")
        fields["category"] = "随便放一个分类"

        with self.assertRaisesRegex(ValueError, "不支持的分类"):
            ingest_issue.validate_submission_fields(fields)

    def test_all_category_mappings_are_stable(self):
        expected = {
            "AI Shock": "ai-shock",
            "AI + 专业方法论": "ai-professional",
            "整活 Skill": "fun-skills",
            "库维护工具": "library-tools",
        }

        for category, directory in expected.items():
            normalized = ingest_issue.normalize_category(category)
            self.assertEqual(ingest_issue.CATEGORY_DIRS[normalized], directory)

    def test_existing_skill_is_not_overwritten_by_another_issue(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fields = fixture_fields("internal_proxy_issue.md")
            first = ingest_issue.write_skill_package(root, fields, "10")
            second = ingest_issue.write_skill_package(root, fields, "11")

            self.assertEqual(first.name, "event-retrospective")
            self.assertEqual(second.name, "event-retrospective-issue-11")
            first_metadata = json.loads(
                (first / "skill.json").read_text(encoding="utf-8")
            )
            second_metadata = json.loads(
                (second / "skill.json").read_text(encoding="utf-8")
            )
            self.assertEqual(first_metadata["source_issue"], 10)
            self.assertEqual(second_metadata["source_issue"], 11)

    def test_same_issue_updates_its_draft_and_rebuilds_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fields = fixture_fields("external_claude_issue.md")
            first = ingest_issue.write_skill_package(
                root, fields, "51", "outside-user"
            )
            fields["author"] = "Updated Contributor"
            second = ingest_issue.write_skill_package(
                root, fields, "51", "outside-user"
            )
            ingest_issue.rebuild_index(root)

            self.assertEqual(first, second)
            metadata = json.loads(
                (second / "skill.json").read_text(encoding="utf-8")
            )
            index = json.loads(
                (root / "index" / "skills.json").read_text(encoding="utf-8")
            )
            self.assertEqual(metadata["author"], "Updated Contributor")
            self.assertEqual(metadata["github"], "outside-user")
            self.assertEqual(index[0]["name"], "meeting-action-items")

    def test_reviewed_submission_requires_publication_confirmation(self):
        with tempfile.TemporaryDirectory() as tmp:
            skills_root = Path(tmp) / "skills"
            skill_dir = skills_root / "ai-shock" / "pending-publication"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                "---\n"
                "name: pending-publication\n"
                'description: "Use when testing publication review requirements."\n'
                "---\n\n"
                "# Pending Publication\n",
                encoding="utf-8",
            )
            (skill_dir / "skill.json").write_text(
                json.dumps(
                    {
                        "name": "pending-publication",
                        "category": "AI Shock",
                        "author": "Contributor",
                        "tags": [],
                        "status": "reviewed",
                        "platforms": ["codex"],
                        "publication_status": "需进一步核查",
                        "submission_type": "external-codex",
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            errors = validate_skills.validate_skill(skill_dir, skills_root)

        self.assertTrue(
            any("must be confirmed suitable for publication" in error for error in errors)
        )


if __name__ == "__main__":
    unittest.main()
