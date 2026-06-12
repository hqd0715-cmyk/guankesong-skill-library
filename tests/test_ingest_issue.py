import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INGEST_PATH = ROOT / "scripts" / "ingest_issue.py"
VALIDATE_PATH = ROOT / "scripts" / "validate_skills.py"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ingest_issue = load_module("ingest_issue", INGEST_PATH)
validate_skills = load_module("validate_skills", VALIDATE_PATH)


class InternalProxySubmissionTest(unittest.TestCase):
    def test_issue_fields_are_preserved_in_metadata(self):
        body = """### Skill 标题
活动复盘助手

### Skill 英文 ID
event-retrospective

### 分类
AI + 专业方法论

### 作者 / 公开署名
莞客松围炉会共创

### 原始提供者
围炉会参与者

### 素材来源
2026 莞客松围炉会

### 整理人
莞客松整理组

### GitHub 用户名
_No response_

### 标签
活动复盘, 工作流

### 难度
beginner

### 适用场景
活动结束后整理复盘材料。

### 使用步骤
1. 汇总记录。
2. 生成复盘。

### Prompt 示例
请根据以下记录生成活动复盘。

### 注意事项
删除个人隐私。

### 案例
围炉会活动复盘。

### 公开状态
已确认适合公开
"""
        fields = {
            key: ingest_issue.clean_value(value)
            for key, value in ingest_issue.parse_issue_form(body).items()
        }
        metadata = ingest_issue.metadata_json("event-retrospective", fields, "42")

        self.assertEqual(metadata["author"], "莞客松围炉会共创")
        self.assertEqual(metadata["provider"], "围炉会参与者")
        self.assertEqual(metadata["source"], "2026 莞客松围炉会")
        self.assertEqual(metadata["curator"], "莞客松整理组")
        self.assertEqual(metadata["publication_status"], "已确认适合公开")
        self.assertEqual(metadata["submission_mode"], "internal-proxy")
        self.assertEqual(metadata["source_issue"], 42)

    def test_internal_proxy_metadata_requires_provenance(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = root / "skills"
            skill_dir = skills_root / "ai-shock" / "missing-provenance"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                "---\n"
                "name: missing-provenance\n"
                'description: "Use when testing internal proxy submission metadata requirements."\n'
                "---\n\n"
                "# Missing Provenance\n",
                encoding="utf-8",
            )
            (skill_dir / "skill.json").write_text(
                json.dumps(
                    {
                        "name": "missing-provenance",
                        "category": "AI Shock",
                        "author": "莞客松团队",
                        "tags": [],
                        "platforms": ["codex"],
                        "submission_mode": "internal-proxy",
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            errors = validate_skills.validate_skill(skill_dir, skills_root)

        self.assertTrue(any("provider is required" in error for error in errors))
        self.assertTrue(any("source is required" in error for error in errors))
        self.assertTrue(any("curator is required" in error for error in errors))
        self.assertTrue(any("publication_status is required" in error for error in errors))

    def test_reviewed_proxy_submission_requires_publication_confirmation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = root / "skills"
            skill_dir = skills_root / "ai-shock" / "pending-publication"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                "---\n"
                "name: pending-publication\n"
                'description: "Use when testing publication review requirements for proxy submissions."\n'
                "---\n\n"
                "# Pending Publication\n",
                encoding="utf-8",
            )
            (skill_dir / "skill.json").write_text(
                json.dumps(
                    {
                        "name": "pending-publication",
                        "category": "AI Shock",
                        "author": "莞客松团队",
                        "provider": "活动参与者",
                        "source": "莞客松活动",
                        "curator": "莞客松整理组",
                        "tags": [],
                        "status": "reviewed",
                        "platforms": ["codex"],
                        "publication_status": "需进一步核查",
                        "submission_mode": "internal-proxy",
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
