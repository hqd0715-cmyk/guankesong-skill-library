import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUBMIT_SCRIPT = ROOT / "skills" / "library-tools" / "submit-skills" / "scripts" / "submit_skills.py"


class SubmitSkillsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.repo = self.base / "library"
        self.repo.mkdir()
        (self.repo / "scripts").mkdir()
        (self.repo / "skills").mkdir()
        shutil.copy(ROOT / "scripts" / "ingest_issue.py", self.repo / "scripts" / "ingest_issue.py")
        shutil.copy(ROOT / "scripts" / "validate_skills.py", self.repo / "scripts" / "validate_skills.py")
        self._run(["git", "init", "-q", "-b", "main"], cwd=self.repo)
        self._run(["git", "config", "user.email", "test@example.com"], cwd=self.repo)
        self._run(["git", "config", "user.name", "Test User"], cwd=self.repo)
        self._run(["git", "add", "."], cwd=self.repo)
        self._run(["git", "commit", "-q", "-m", "initial"], cwd=self.repo)

    def tearDown(self):
        self.tmp.cleanup()

    def _run(self, command, cwd=None):
        result = subprocess.run(
            command,
            cwd=cwd,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
        if result.returncode != 0:
            self.fail(
                f"Command failed: {' '.join(map(str, command))}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
            )
        return result

    def _write_skill(self, skill_dir: Path, name="sample-skill", author="Original Author"):
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(
            "\n".join(
                [
                    "---",
                    f"name: {name}",
                    'description: "Use when testing submit-skills formal copy and commit paths."',
                    "---",
                    "",
                    "# Sample Skill",
                    "",
                    "Follow a small deterministic workflow.",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        (skill_dir / "skill.json").write_text(
            json.dumps(
                {
                    "name": name,
                    "title": "Sample Skill",
                    "category": "AI Shock",
                    "author": author,
                    "github": "original",
                    "tags": ["test"],
                    "status": "draft",
                    "created": "2026-06-04",
                    "updated": "2026-06-04",
                    "difficulty": "beginner",
                    "platforms": ["codex"],
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    def test_external_skill_submission_commits_copied_skill(self):
        source = self.base / "source" / "sample-skill"
        self._write_skill(source)

        self._run(
            [
                sys.executable,
                str(SUBMIT_SCRIPT),
                "--source",
                str(source),
                "--repo-dir",
                str(self.repo),
                "--author",
                "Tester",
                "--github",
                "tester",
                "--branch",
                "skill-submission/test-external",
                "--message",
                "test external submission",
            ]
        )

        target = self.repo / "skills" / "ai-shock" / "sample-skill"
        self.assertTrue((target / "SKILL.md").exists())
        metadata = json.loads((target / "skill.json").read_text(encoding="utf-8"))
        self.assertEqual(metadata["author"], "Tester")
        index = json.loads((self.repo / "index" / "skills.json").read_text(encoding="utf-8"))
        self.assertEqual(index[0]["name"], "sample-skill")
        self.assertIn("test external submission", self._run(["git", "log", "-1", "--format=%s"], cwd=self.repo).stdout)

    def test_in_place_skill_submission_updates_metadata(self):
        target = self.repo / "skills" / "ai-shock" / "sample-skill"
        self._write_skill(target)
        self._run(["git", "add", "."], cwd=self.repo)
        self._run(["git", "commit", "-q", "-m", "add sample skill"], cwd=self.repo)

        self._run(
            [
                sys.executable,
                str(SUBMIT_SCRIPT),
                "--source",
                str(target),
                "--repo-dir",
                str(self.repo),
                "--author",
                "Updated Tester",
                "--github",
                "updated-tester",
                "--branch",
                "skill-submission/test-in-place",
                "--message",
                "test in-place submission",
            ]
        )

        metadata = json.loads((target / "skill.json").read_text(encoding="utf-8"))
        self.assertEqual(metadata["author"], "Updated Tester")
        self.assertEqual(metadata["github"], "updated-tester")
        self.assertIn("test in-place submission", self._run(["git", "log", "-1", "--format=%s"], cwd=self.repo).stdout)


if __name__ == "__main__":
    unittest.main()
