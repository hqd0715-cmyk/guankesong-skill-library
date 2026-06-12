---
name: "submit-skills"
description: "Organize internally curated Agent Skill packages and submit them to the Guankesong Skill Library review branch. Use when a Guankesong maintainer asks to proxy-submit, import, publish, push, or organize local Codex or Claude Code skills for internal review. Basic dry-run, copy, validate, and commit steps do not require GitHub CLI; only Draft PR creation requires gh."
---

# Submit Skills

Use this skill when an internal Guankesong maintainer has already collected and curated one or more Agent Skill packages. Copy them into the library category structure, rebuild the index, validate the repository, and optionally commit, push, or create a Draft PR.

## Workflow

1. Confirm the source folder contains standard skill packages. Each skill package must include `SKILL.md`; its frontmatter must contain only `name` and `description`.
2. Confirm attribution and provenance. Each skill should have `skill.json.author`, plus `source_provider`, `source`, `curator`, `publication_status`, and `submission_type` for internal proxy submissions. Pass `--author` and `--github` only to override contributor identity when appropriate; do not replace the original provider with the maintainer's account.
3. Confirm the target repository is a local `guankesong-skill-library` checkout and the worktree is clean unless the user explicitly allows `--allow-dirty`.
4. Run a dry-run first:

```bash
python "${CLAUDE_SKILL_DIR:-skills/library-tools/submit-skills}/scripts/submit_skills.py" --source <skills-to-submit> --repo-dir <library-repo> --author <author> --github <github-user> --dry-run
```

```powershell
$skillDir = if ($env:CLAUDE_SKILL_DIR) { $env:CLAUDE_SKILL_DIR } else { "skills\library-tools\submit-skills" }
python "$skillDir\scripts\submit_skills.py" --source <skills-to-submit> --repo-dir <library-repo> --author <author> --github <github-user> --dry-run
```

5. If the dry-run is correct, create the review branch and local commit:

```bash
python "${CLAUDE_SKILL_DIR:-skills/library-tools/submit-skills}/scripts/submit_skills.py" --source <skills-to-submit> --repo-dir <library-repo> --author <author> --github <github-user>
```

```powershell
$skillDir = if ($env:CLAUDE_SKILL_DIR) { $env:CLAUDE_SKILL_DIR } else { "skills\library-tools\submit-skills" }
python "$skillDir\scripts\submit_skills.py" --source <skills-to-submit> --repo-dir <library-repo> --author <author> --github <github-user>
```

6. Add `--push` only when the user explicitly asks to push the branch. Add `--create-pr` only when GitHub CLI is installed and the user wants an automatic Draft PR:

```bash
python "${CLAUDE_SKILL_DIR:-skills/library-tools/submit-skills}/scripts/submit_skills.py" --source <skills-to-submit> --repo-dir <library-repo> --author <author> --github <github-user> --push --create-pr
```

## Submission Rules

- Submit only standard Agent Skill packages. Do not copy temporary files, `.git`, `node_modules`, `__pycache__`, build artifacts, virtual environments, or generated caches into the library.
- Do not require GitHub CLI for dry-run, copy, validation, or local commit. Treat `gh` as optional and only required for `--create-pr`.
- Do not submit skills without contributor information. Prefer explicit `--author` and `--github`; use `gh` profile data only as a fallback.
- Do not use this local-copy tool as the external intake endpoint. External contributors should create standardized Issues; raw material selected for this internal path must be screened by an internal curator.
- Preserve original `source_provider`, `source`, `curator`, and publication-review metadata in `skill.json`.
- Do not silently move a skill that already exists under another category. Use `--replace-existing` only when the user explicitly wants to move it.
- Before push, inspect `git diff --stat` and `git status --short`.
- If the library worktree has uncommitted changes, stop unless the user explicitly allows `--allow-dirty`.
- Commit messages should use `YYYY-MM-DD HH:mm～中文变更描述`.

## Script Behavior

`scripts/submit_skills.py` scans local skill packages, applies contributor metadata to the copied package, places each skill under `skills/<category>/<name>/`, rebuilds `index/skills.json`, validates the repository, and commits only the copied skill paths plus the index.

Supported categories are:

- `AI Shock` -> `skills/ai-shock`
- `AI + 专业方法论` -> `skills/ai-professional`
- `整活 Skill` -> `skills/fun-skills`
- `库维护工具` -> `skills/library-tools`
