---
name: "submit-skills"
description: "整理当前文件夹中的标准 Agent Skills，并把它们提交到莞客松 Skill 共创库的审核分支。Use when the user asks to submit, contribute, publish, push, or organize local Codex or Claude Code skills for review in this GitHub skill library."
---

# Submit Skills

## 工作流

1. 确认当前目录或用户指定目录中存在标准 Agent Skill 包：每个 skill 目录必须包含 `SKILL.md`，且 frontmatter 只有 `name` 和 `description`。
2. 确认每个 skill 的 `skill.json` 里有贡献者信息：`author` 必填，`github` 建议填写。不想手动改 `skill.json` 时，在脚本里传 `--author` 和 `--github`。如果没有传 `--github`，脚本会尝试读取当前 `gh` 登录账号。
3. 克隆或进入莞客松 Skill 共创库，并保持工作区干净。
4. 先执行 dry-run，查看会提交哪些 skill 和贡献者：

```bash
python "${CLAUDE_SKILL_DIR:-skills/library-tools/submit-skills}/scripts/submit_skills.py" --source <待投稿目录> --repo-dir <共创库目录> --author <作者昵称> --github <GitHub用户名> --dry-run
```

```powershell
$skillDir = if ($env:CLAUDE_SKILL_DIR) { $env:CLAUDE_SKILL_DIR } else { "skills\library-tools\submit-skills" }
python "$skillDir\scripts\submit_skills.py" --source <待投稿目录> --repo-dir <共创库目录> --author <作者昵称> --github <GitHub用户名> --dry-run
```

5. 如果结果正确，再创建审核分支并提交：

```bash
python "${CLAUDE_SKILL_DIR:-skills/library-tools/submit-skills}/scripts/submit_skills.py" --source <待投稿目录> --repo-dir <共创库目录> --author <作者昵称> --github <GitHub用户名>
```

```powershell
$skillDir = if ($env:CLAUDE_SKILL_DIR) { $env:CLAUDE_SKILL_DIR } else { "skills\library-tools\submit-skills" }
python "$skillDir\scripts\submit_skills.py" --source <待投稿目录> --repo-dir <共创库目录> --author <作者昵称> --github <GitHub用户名>
```

6. 用户明确要求推送或等待审核时，再加 `--push`。如果本机已登录 GitHub CLI，可以同时加 `--create-pr` 创建 Draft PR：

```bash
python "${CLAUDE_SKILL_DIR:-skills/library-tools/submit-skills}/scripts/submit_skills.py" --source <待投稿目录> --repo-dir <共创库目录> --author <作者昵称> --github <GitHub用户名> --push --create-pr
```

```powershell
$skillDir = if ($env:CLAUDE_SKILL_DIR) { $env:CLAUDE_SKILL_DIR } else { "skills\library-tools\submit-skills" }
python "$skillDir\scripts\submit_skills.py" --source <待投稿目录> --repo-dir <共创库目录> --author <作者昵称> --github <GitHub用户名> --push --create-pr
```

## 提交规则

- 只提交标准 Agent Skill 包，不把临时文件、`.git`、`node_modules`、`__pycache__`、构建产物或虚拟环境复制进仓库。
- 不提交没有作者信息的 skill；没有 `skill.json.author` 时会优先使用 `--author`，其次使用当前 GitHub profile name 或 login。
- 推送前必须检查 `git diff --stat` 和 `git status --short`。
- 如果共创库已有未提交改动，先停下确认，除非用户明确允许混合处理。
- 提交信息必须使用 `YYYY-MM-DD HH:mm｜中文变更描述` 格式。

## 资源

- `scripts/submit_skills.py`：扫描本地 Agent Skill 包、按 `skill.json.category` 复制到共创库 `skills/<category>/<name>/`、刷新索引、校验结构、提交分支，并可选推送或创建 Draft PR。
