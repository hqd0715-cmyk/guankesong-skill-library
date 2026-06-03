# 莞客松 Skill 共创库

这是一个面向外部成员投稿、内部成员审核整理的 Agent Skill 共创库。仓库目标是把大家沉淀下来的 AI 用法、专业方法论和有趣玩法，整理成可检索、可复用、可在 Codex 和 Claude Code 之间迁移的 skill 包。

## Skill 包结构

每个 skill 必须是 `skills/` 下的直接子目录：

```text
skills/
└── your-skill-name/
    ├── SKILL.md          # 必需：Agent Skill 入口，只包含通用 name/description frontmatter
    ├── skill.json        # 建议：共创库索引元数据
    ├── agents/           # 可选：OpenAI UI 元数据
    ├── scripts/          # 可选：确定性脚本
    ├── references/       # 可选：按需加载的参考资料
    └── assets/           # 可选：模板、图片、字体等资源
```

`SKILL.md` 的 YAML frontmatter 只保留 Codex 和 Claude Code 都能稳定理解的共同字段：

```yaml
---
name: "your-skill-name"
description: "说明这个 skill 做什么，以及什么时候使用。"
---
```

分类、作者、标签、审核状态等不要塞进 `SKILL.md`，统一放在同目录的 `skill.json`。

## 兼容原则

本仓库采用 Codex skills 和 Claude Code skills 的最小共同结构：

- 每个 skill 是一个独立目录，目录内必须有 `SKILL.md`。
- `SKILL.md` frontmatter 只允许 `name` 和 `description`。
- `name` 使用小写字母、数字和连字符，并与目录名一致。
- `description` 同时说明能力和触发场景，避免只写标题。
- `scripts/`、`references/`、`assets/` 等资源目录可以按需存在。
- Claude Code 专属字段和本库索引字段不要写进 `SKILL.md`；索引信息放进 `skill.json`。

更细的兼容说明见 [兼容性说明](docs/compatibility.md)。

## 分类

| 分类 | 适合内容 |
| --- | --- |
| AI Shock | AI 信息差、爆款 Prompt、工具新玩法、效率技巧 |
| AI + 专业方法论 | AI + 活动策划、能源动力、简历优化、数据分析等专业工作流 |
| 整活 Skill | 表情包、海报、小游戏、视频脚本、创意玩法 |
| 库维护工具 | 投稿、校验、索引等仓库维护 skill |

## 投稿方式

### 方式一：Issue 投稿

1. 进入仓库 Issues 页面。
2. 选择 `Skill 投稿` 表单。
3. 填写标题、分类、作者、标签、适用场景、步骤、Prompt 和案例。
4. GitHub Actions 会生成 `skills/<skill-name>/SKILL.md` 和 `skill.json`，并自动创建 Draft PR。
5. 内部成员审核、修改、刷新索引后合并到 `main`。

### 方式二：本地 Agent Skill 包投稿

仓库内置 `submit-skills`：

```bash
python skills/submit-skills/scripts/submit_skills.py --source <你的skills目录> --repo-dir . --dry-run
python skills/submit-skills/scripts/submit_skills.py --source <你的skills目录> --repo-dir . --push --create-pr
```

第二条命令会整理本地标准 Agent Skill 包、刷新索引、创建审核分支，并在本机 GitHub 权限可用时创建 Draft PR。

## 本地维护

刷新索引：

```bash
python scripts/ingest_issue.py --rebuild-index
```

校验 skill 结构：

```bash
python scripts/validate_skills.py
```

合并前建议执行：

```bash
python scripts/ingest_issue.py --rebuild-index
python scripts/validate_skills.py
git diff --check
```

## 文件结构

```text
.
├── skills/
│   ├── submit-skills/
│   ├── government-institution-text-polish/
│   └── ...
├── templates/
│   └── skill/
│       ├── SKILL.md
│       └── skill.json
├── index/
│   └── skills.json
├── docs/
├── scripts/
│   ├── ingest_issue.py
│   └── validate_skills.py
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   └── skill_submission.yml
│   └── workflows/
│       └── skill-submission-to-pr.yml
├── index.html
└── README.md
```

## GitHub Pages

仓库内置轻量展示页 `index.html`，会读取 `index/skills.json` 展示已合并 skill。启用方式：

1. 进入仓库 `Settings`。
2. 打开 `Pages`。
3. Source 选择 `Deploy from a branch`。
4. Branch 选择 `main`，目录选择 `/root`。
