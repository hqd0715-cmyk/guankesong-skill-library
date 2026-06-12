import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CatalogPageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.guide = (ROOT / "docs" / "external-skill-usage.md").read_text(
            encoding="utf-8"
        )

    def test_public_catalog_defaults_to_reviewed_skills(self):
        self.assertIn('skill.status === "reviewed"', self.page)
        self.assertIn('skill.category !== "库维护工具"', self.page)
        self.assertIn('.get("status") === "all"', self.page)

    def test_main_catalog_prefers_single_index_request(self):
        self.assertIn('if (currentRef() === "main")', self.page)
        index_position = self.page.index("return await loadSkillsFromIndex();")
        repository_position = self.page.index(
            "return await loadSkillsFromRepository();", index_position
        )
        self.assertLess(index_position, repository_position)

    def test_catalog_exposes_search_and_client_prompts(self):
        self.assertIn("复制 Agent 检索提示词", self.page)
        self.assertIn("复制 Codex 取用提示词", self.page)
        self.assertIn("复制 Claude Code 取用提示词", self.page)
        self.assertIn("不能只复制 SKILL.md", self.page)

    def test_usage_guide_covers_both_clients_and_full_directory(self):
        self.assertIn("## Codex 取用", self.guide)
        self.assertIn("## Claude Code 取用", self.guide)
        self.assertIn("index/skills.json", self.guide)
        self.assertIn("不要只下载 `SKILL.md`", self.guide)


if __name__ == "__main__":
    unittest.main()
