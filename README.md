# 莞客松 Skill 共创库

这是莞客松团队用于收集、整理、审核和发布 Agent Skill 的共创知识库。仓库目标是把活动、围炉会、社群交流和真实项目中沉淀的 AI 用法、专业方法论与创意玩法，整理成可检索、可复用、可在 Codex 和 Claude Code 之间迁移的 Skill 包。

仓库采用双入口：内部成员代投稿是主要质量通道；外部贡献者也可以让 Claude Code、Codex 或 GitHub CLI 创建标准化 Issue。外部投稿不需要 fork、clone、push 或自行创建 PR。

更准确地说，本库采用“内部整理为主、外部 Agent 投稿为辅”的机制，不是无需审核的开放投稿平台。

```text
内部素材 → 内部整理 → 内部代投稿 Issue ┐
                                         ├→ 自动生成 Draft PR → 维护者审核 → CI → 合并
外部 Skill → Agent 创建标准化 Issue ────┘
```

所有自动生成的 PR 都是 Draft，不会自动合并。详见 [内部代投稿指南](docs/internal-proxy-submission.md)、[外部 Agent 投稿指南](docs/external-agent-submission.md) 和 [审核指南](docs/review-guide.md)。

## 快速开始

1. 打开 [GitHub Pages 展示页](https://hqd0715-cmyk.github.io/guankesong-skill-library/)。
2. 搜索任务关键词，默认只查看已审核的 `reviewed` Skill。
3. 点击卡片中的按钮，复制 Codex 或 Claude Code 取用提示词。
4. 让本地 Agent 安装完整 Skill 目录。
5. 重启或重新加载客户端；需要强制触发时，可明确写出 Skill 名称。

不要只复制 `SKILL.md`。Skill 可能依赖同目录下的 `scripts/`、`references/`、`assets/` 或 `agents/`。

不知道该选哪个 Skill 时，可以让 Agent 读取 `index/skills.json` 后按任务推荐。完整流程和可复制提示词见 [外部成员检索与取用指南](docs/external-skill-usage.md)。

## Skill 包结构

每个 skill 必须放在对应大类目录下：

```text
skills/
└── ai-professional/
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

### Codex 安装

复制具体 Skill 目录到：

- 用户级：`$CODEX_HOME/skills/<skill-name>/`
- 未设置 `CODEX_HOME` 时：`~/.codex/skills/<skill-name>/`

Windows PowerShell 示例：

```powershell
Copy-Item -Recurse `
  .\skills\ai-shock\wechat-official-account-writer `
  "$HOME\.codex\skills\wechat-official-account-writer"
```

### Claude Code 安装

复制具体 Skill 目录到：

- 用户级：`~/.claude/skills/<skill-name>/`
- 项目级：`.claude/skills/<skill-name>/`

共创库内部保留大类目录用于审核和检索；安装时只复制具体 Skill 目录，不复制 `ai-shock` 等分类目录。

## 分类

| 分类 | 适合内容 |
| --- | --- |
| AI Shock | AI 信息差、爆款 Prompt、工具新玩法、效率技巧 |
| AI + 专业方法论 | AI + 活动策划、能源动力、简历优化、数据分析等专业工作流 |
| 整活 Skill | 表情包、海报、小游戏、视频脚本、创意玩法 |
| 库维护工具 | 投稿、校验、索引等仓库维护 skill |

## 审核状态

`skill.json.status` 表示仓库审核状态：

- `draft`：自动生成或仍待补充，不能视为稳定推荐。
- `reviewed`：已由维护者检查结构、内容与公开合规性。

合并正式 Skill 前，应将状态更新为 `reviewed`；确需保留草稿时，应在 PR 中说明原因。

## 投稿方式

### 方式一：内部成员代投稿 Issue

1. 先从活动、群聊、访谈、问卷或飞书文档中收集素材。
2. 由整理人完成筛选、去重、改写、风险检查和格式标准化。
3. 内部成员进入仓库 Issues 页面，选择 `内部 Skill 代投稿` 表单。
4. 填写标题、分类、原始提供者、素材来源、整理人、适用场景、步骤、Prompt 和案例。
5. GitHub Actions 会按分类生成 `skills/<category>/<skill-name>/SKILL.md` 和 `skill.json`，并自动创建 Draft PR。
6. 内部成员审核、修改、刷新索引后合并到 `main`。

Issue 自动化会校验 `internal-proxy` 提交者的仓库权限。只有拥有 `write`、`maintain` 或 `admin` 权限的内部成员才能使用这个入口。

### 方式二：内部成员提交本地 Agent Skill 包

仓库内置 `submit-skills`：

```bash
python skills/library-tools/submit-skills/scripts/submit_skills.py --source <你的skills目录> --repo-dir . --author <作者昵称> --github <GitHub用户名> --dry-run
python skills/library-tools/submit-skills/scripts/submit_skills.py --source <你的skills目录> --repo-dir . --author <作者昵称> --github <GitHub用户名> --push --create-pr
```

第二条命令会整理本地标准 Agent Skill 包，把作者信息写入 `skill.json`，刷新索引、创建审核分支，并在本机 GitHub 权限可用时创建 Draft PR。没有传 `--github` 时，脚本会尝试使用当前 `gh` 登录账号。

### 方式三：外部 Agent 创建 Issue

外部贡献者可以在 Issues 页面选择 `外部 Agent 投稿`，也可以让 Claude Code 或 Codex 调用 GitHub CLI 创建标题以 `[Skill]` 开头的标准化 Issue。支持：

- `external-claude-code`
- `external-codex`
- `external-manual`

系统会生成 `skill-submission/issue-<编号>` 分支和 Draft PR。外部贡献者没有仓库写权限，也无需接触 Git 分支；维护者负责核查、修改和决定是否合并。

完整命令、正文模板和 Agent 提示词见 [外部 Agent 投稿指南](docs/external-agent-submission.md)。

### 方式四：提供原始素材

不使用 GitHub 的参与者仍可通过团队指定的飞书表格、问卷、活动记录或社群渠道提供原始素材，由内部整理人筛选后代投稿。

网络公开内容只能作为参考素材。入库前应重新组织和改写，并标明来源，避免大段复制原文。

## 本地维护

刷新索引：

```bash
python scripts/ingest_issue.py --rebuild-index
```

校验 skill 结构：

```bash
python scripts/validate_skills.py
```

运行回归测试：

```bash
python -m unittest discover -s tests -p "test_*.py"
```

合并前建议执行：

```bash
python scripts/ingest_issue.py --rebuild-index
python scripts/validate_skills.py
python -m unittest discover -s tests -p "test_*.py"
git diff --check
git diff --exit-code index/skills.json
```

普通 Pull Request 会由 `.github/workflows/validate-repository.yml` 自动执行同类检查。索引未刷新、Skill 结构不合法、测试失败或存在空白错误时，PR 校验会失败。

## 文件结构

```text
.
├── skills/
│   ├── ai-shock/
│   ├── ai-professional/
│   ├── fun-skills/
│   └── library-tools/
├── templates/
│   └── skill/
│       ├── SKILL.md
│       └── skill.json
├── index/
│   └── skills.json
├── docs/
│   ├── external-agent-submission.md
│   ├── external-skill-usage.md
│   ├── internal-proxy-submission.md
│   ├── internal-operations.md
│   ├── review-guide.md
│   ├── branch-protection.md
│   └── e2e-test-checklist.md
├── scripts/
│   ├── ingest_issue.py
│   └── validate_skills.py
├── tests/
│   ├── fixtures/
│   ├── test_ingest_issue.py
│   └── test_submit_skills.py
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── internal_proxy_submission.yml
│   │   └── external_agent_submission.yml
│   └── workflows/
│       ├── skill-submission-to-pr.yml
│       └── validate-repository.yml
├── index.html
└── README.md
```

## GitHub Pages

仓库内置轻量展示页 `index.html`，会优先通过 GitHub API 实时读取 `skills/<category>/<skill-name>/SKILL.md` 和 `skill.json`，失败时回退到 `index/skills.json`。默认读取 `main` 分支，也可以用 `?ref=<branch>` 预览其他分支，例如 `?ref=rebuild-standard-skill-library`。

`index/skills.json` 仍建议保留并随投稿刷新，作为 GitHub API 限流、网络失败或本地静态预览时的兜底数据。

启用方式：

1. 进入仓库 `Settings`。
2. 打开 `Pages`。
3. Source 选择 `Deploy from a branch`。
4. Branch 选择 `main`，目录选择 `/root`。

启用后默认地址为：

`https://hqd0715-cmyk.github.io/guankesong-skill-library/`
