# 外部 Agent 投稿指南

## 原则

外部贡献者只创建标准化 GitHub Issue：

- 不 fork 仓库。
- 不 clone 仓库。
- 不 push 分支。
- 不直接创建 Pull Request。
- 不需要仓库写权限。

GitHub Actions 会把合格 Issue 转换为投稿 PR，并在原 Issue 下评论 PR 链接。莞客松维护者负责审核、修改和决定是否合并；只有 PR 合并后，Skill 才会进入共创库页面。

## 投稿前准备

安装并登录 GitHub CLI：

```bash
gh auth status
```

如果尚未登录：

```bash
gh auth login
```

## 直接使用网页

进入仓库 `Issues → New issue → 外部 Agent 投稿`，填写表单并选择：

- Claude Code：`external-claude-code`
- Codex：`external-codex`
- 其他方式：`external-manual`

## 使用 Claude Code

把下面提示词直接交给 Claude Code：

```text
请把我接下来提供的 Agent Skill 整理成莞客松 Skill 共创库的标准化 GitHub Issue。
仓库是 hqd0715-cmyk/guankesong-skill-library。
只允许创建 Issue，不要 fork、clone、push 或创建 Pull Request。
先运行 gh auth status。然后生成 issue-body.md，必须使用三级标题并依次包含：
Skill 标题、Skill 英文 ID、分类、作者 / 公开署名、原始提供者、素材来源、
整理人、GitHub 用户名、标签、难度、适用场景、使用步骤、Prompt 示例、
注意事项、案例、公开状态、投稿方式。
投稿方式固定写 external-claude-code，Issue 标题以 [Skill] 开头。
最后运行 gh issue create --repo hqd0715-cmyk/guankesong-skill-library
--title "[Skill] <Skill 标题>" --body-file issue-body.md，并告诉我 Issue URL。
不要执行其他 GitHub 写操作。
```

## 使用 Codex

把下面提示词直接交给 Codex：

```text
请审查并整理我提供的 Agent Skill，然后只通过 GitHub Issue 投稿到
hqd0715-cmyk/guankesong-skill-library。
不要 fork、clone、push、创建分支或创建 Pull Request。
先检查 gh auth status。将正文写入 issue-body.md，使用仓库要求的三级标题字段：
Skill 标题、Skill 英文 ID、分类、作者 / 公开署名、原始提供者、素材来源、
整理人、GitHub 用户名、标签、难度、适用场景、使用步骤、Prompt 示例、
注意事项、案例、公开状态、投稿方式。
投稿方式固定写 external-codex；标题必须以 [Skill] 开头。
缺少非核心来源字段时保留为空或写“需进一步核查”，不要编造。
创建 Issue 后返回 URL，并停止，不要直接改仓库。
```

## GitHub CLI 正文模板

将以下内容保存为 `issue-body.md`：

```markdown
### Skill 标题
填写标题

### Skill 英文 ID
optional-kebab-case-id

### 分类
AI Shock

### 作者 / 公开署名
填写署名

### 原始提供者
同作者

### 素材来源
原创

### 整理人

### GitHub 用户名

### 标签
tag-one, tag-two

### 难度
beginner

### 适用场景
说明何时使用。

### 使用步骤
1. 第一步。
2. 第二步。

### Prompt 示例
填写可复制的 Prompt；没有 Prompt 时可留空。

### 注意事项
填写风险、限制或依赖。

### 案例
填写真实或可复现案例。

### 公开状态
需进一步核查

### 投稿方式
external-manual
```

创建 Issue：

```bash
gh issue create \
  --repo hqd0715-cmyk/guankesong-skill-library \
  --title "[Skill] 填写 Skill 标题" \
  --body-file issue-body.md
```

不必添加标签；`[Skill]` 标题前缀会触发自动化。

## 提交后

1. `Skill submission to PR` 工作流解析 Issue。
2. 系统创建或更新 `skill-submission/issue-<编号>` 分支。
3. 系统创建或更新投稿 PR，并在原 Issue 下评论 PR 链接。
4. 系统显式触发仓库校验。
5. 维护者检查内容、来源、公开风险、重复度和兼容性。
6. 维护者可要求补充、修改后合并，或关闭不合适的投稿。
7. PR 合并到 `main` 且 GitHub Pages 部署完成后，Skill 才会出现在共创库页面。

编辑原 Issue 会重新生成同一分支并更新原投稿 PR，不会重复创建 PR。Issue 创建成功不等于已经入库；请以 Issue 下的 PR 链接和 PR 合并状态为准。

## 常见问题

- Action 未运行：确认 Issue 标题以 `[Skill]` 开头，或联系维护者手动运行工作流。
- 解析失败：检查字段标题是否使用 `###`，以及标题、分类、作者、适用场景、使用步骤是否齐全。
- 英文 ID 失败：只使用小写字母、数字和连字符，不包含 `anthropic` 或 `claude`。
- 分类失败：使用 `AI Shock`、`AI + 专业方法论` 或 `整活 Skill`。
- CI 通过但未合并：CI 只验证结构，是否收录仍由维护者决定。
- 共创库页面搜不到：先确认对应 PR 已合并到 `main`，再检查 Pages 部署状态。
