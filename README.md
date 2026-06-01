# 莞客松 Skill 共创库

这是一个面向外部成员投稿、内部成员审核整理的 GitHub Skill 仓库。目标是把大家沉淀下来的 AI 用法、专业方法论和有趣玩法，整理成可检索、可复用、可持续维护的知识库。

## 三类 Skill

| 分类 | 目录 | 适合内容 |
| --- | --- | --- |
| AI Shock | `skills/ai-shock/` | AI 信息差、爆款 Prompt、工具新玩法、效率技巧 |
| AI + 专业方法论 | `skills/ai-professional/` | AI + 活动策划、能源动力、简历优化、数据分析等专业工作流 |
| 整活 Skill | `skills/fun-skills/` | 表情包、海报、小游戏、视频脚本、创意玩法 |

## 投稿流程

1. 进入仓库的 Issues 页面。
2. 选择 `Skill 投稿` 表单。
3. 填写标题、分类、作者、标签、适用场景、步骤、Prompt 和案例。
4. GitHub Actions 会把投稿整理成 Markdown 文件，并自动创建 Draft Pull Request。
5. 内部成员审核、修改、补全索引后合并到 `main`。

外部成员默认不直接写入 `main`。他们可以通过 Issue 投稿、Fork 后 PR、或继续修改自己的 PR 来更新内容。

## 内部审核标准

| 标准 | 说明 |
| --- | --- |
| 完整 | 有标题、场景、步骤、Prompt 或案例 |
| 可复现 | 按照步骤能跑通 |
| 清晰 | 表述明确，不需要额外猜测 |
| 合规 | 原创或已获授权，没有敏感和无关内容 |
| 分类准确 | 分类、标签和难度适合检索 |

更多细节见 [审核指南](docs/review-guide.md)。

## 文件结构

```text
.
├── skills/
│   ├── ai-shock/
│   ├── ai-professional/
│   └── fun-skills/
├── contributors/
├── templates/
│   └── skill.md
├── index/
│   └── skills.json
├── docs/
├── scripts/
│   └── ingest_issue.py
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   └── skill_submission.yml
│   └── workflows/
│       └── skill-submission-to-pr.yml
├── index.html
└── README.md
```

## 本地维护

生成或刷新索引：

```bash
python scripts/ingest_issue.py --rebuild-index
```

新增 Skill 时建议复制 `templates/skill.md`，并保持 YAML frontmatter 字段完整。

## GitHub Pages

仓库内置了一个轻量展示页 `index.html`，会读取 `index/skills.json` 展示已合并的 Skill。启用方式：

1. 进入仓库 `Settings`。
2. 打开 `Pages`。
3. Source 选择 `Deploy from a branch`。
4. Branch 选择 `main`，目录选择 `/root`。

之后即可通过 GitHub Pages 检索 Skill。
