# 莞客松 Skill 共创库内部与外部操作手册

版本：v1.0

更新日期：2026-06-12

适用仓库：`hqd0715-cmyk/guankesong-skill-library`

## 1. 手册用途

本手册统一说明莞客松 Skill 共创库的检索、取用、投稿、审核和发布流程。

先按身份选择入口：

| 身份 | 可以做什么 | 不应做什么 | 从哪里开始 |
| --- | --- | --- | --- |
| 外部使用者 | 搜索并安装已审核 Skill | 不直接使用未审核草稿 | [GitHub Pages 展示页](https://hqd0715-cmyk.github.io/guankesong-skill-library/) |
| 外部贡献者 | 通过网页、Codex 或 Claude Code 创建投稿 Issue | 不 fork、不 push、不直接创建 PR | `Issues → New issue → 外部 Agent 投稿` |
| 内部整理人 | 收集、去重、改写和核查素材 | 不把代投稿人写成原创者 | [内部运营说明](internal-operations.md) |
| 内部代投稿人 | 提交内部代投稿 Issue 或本地 Skill 包 | 不绕过 Draft PR 和 CI | `Issues → New issue → 内部 Skill 代投稿` |
| 维护者 | 审核 Draft PR、修改状态、合并并验收展示页 | 不因 CI 通过就默认内容合格 | [审核指南](review-guide.md) |

仓库采用双入口，但只有一个发布出口：

```text
内部素材 → 整理与核查 → 内部代投稿 Issue ┐
                                          ├→ Draft PR → 人工审核 → CI → main → Pages
外部贡献 → 标准化外部投稿 Issue ─────────┘
```

自动生成的 Pull Request 默认进入人工审核流程，不会自动合并。Issue 创建成功只代表进入投稿队列；只有 PR 合并到 `main` 并完成 GitHub Pages 部署后，Skill 才会进入共创库页面。

## 2. 外部成员操作

### 2.1 搜索 Skill

1. 打开 [莞客松 Skill 共创库展示页](https://hqd0715-cmyk.github.io/guankesong-skill-library/)。
2. 输入任务关键词，例如“公众号”“公文润色”“审查”“宏观分析”。
3. 按标题、描述、分类、作者、标签、平台或目录查看匹配结果。
4. 默认只选择状态为 `reviewed` 的 Skill。
5. 打开“完整目录”，检查 `SKILL.md` 以及是否包含 `scripts/`、`references/`、`assets/` 或 `agents/`。

不知道选哪个时，点击页面上的“复制 Agent 检索提示词”，交给 Codex 或 Claude Code，并补充自己的任务。

### 2.2 安装和使用 Skill

在 Skill 卡片中选择：

- `复制 Codex 取用提示词`
- `复制 Claude Code 取用提示词`

把提示词交给本地 Agent 后，安装时必须复制整个 Skill 目录，不能只复制 `SKILL.md`。

安装位置：

| 客户端 | 用户级目录 | 项目级目录 |
| --- | --- | --- |
| Codex | `$CODEX_HOME/skills/<skill-name>/`；未设置时为 `~/.codex/skills/<skill-name>/` | 本仓库当前只规定用户级安装 |
| Claude Code | `~/.claude/skills/<skill-name>/` | `.claude/skills/<skill-name>/` |

安装完成后：

1. 确认目标目录存在 `SKILL.md`。
2. 确认附带资源目录没有遗漏。
3. 重启或重新加载客户端。
4. 用自然语言描述对应任务；需要强制触发时，明确写出 Skill 名称。

详细提示词见 [外部成员检索与取用指南](external-skill-usage.md)。

### 2.3 外部投稿

外部成员只创建 Issue，不需要仓库写权限。

允许的方式：

1. 网页：`Issues → New issue → 外部 Agent 投稿`。
2. Codex：让 Codex 整理内容并执行 `gh issue create`。
3. Claude Code：让 Claude Code 整理内容并执行 `gh issue create`。
4. GitHub CLI：按模板手动创建标准化 Issue。

严格限制：

- 不 fork 仓库。
- 不 clone 仓库。
- 不创建分支。
- 不 push 代码。
- 不直接创建 Pull Request。
- Issue 标题以 `[Skill]` 开头。
- Issue 正文使用 `### 字段名` 格式。

投稿方式只能填写：

- `external-codex`
- `external-claude-code`
- `external-manual`

提交后，系统会创建 `skill-submission/issue-<编号>` 分支和投稿 PR，并在原 Issue 下评论 PR 链接。维护者可能要求补充来源、步骤、案例或公开授权；CI 通过不代表一定收录。

完整字段模板和 Agent 提示词见 [外部 Agent 投稿指南](external-agent-submission.md)。

## 3. 内部成员操作

### 3.1 收集与整理素材

内部成员先完成素材治理，再进入 GitHub：

1. 从活动、围炉会、社群、访谈或真实项目中收集素材。
2. 判断内容是否有明确场景、可执行步骤和复用价值。
3. 搜索现有 Skill，避免重复收录。
4. 核查原始提供者、公开署名、素材来源和授权状态。
5. 删除隐私、内部机密和无权公开的内容。
6. 将零散经验改写为场景、输入、步骤、输出、Prompt、限制和案例。

不确定的信息写“需进一步核查”，不要猜测补全。

### 3.2 内部代投稿 Issue

适用于拥有仓库 `write`、`maintain` 或 `admin` 权限的内部成员。

1. 进入 `Issues → New issue → 内部 Skill 代投稿`。
2. 填写原始提供者、素材来源、整理人、适用场景、步骤、Prompt、案例和公开状态。
3. `投稿方式` 选择 `internal-proxy`。
4. 提交后打开 Issue 时间线或 `Actions`，确认 `Skill submission to PR` 已运行。
5. 从 Issue 里的机器人评论打开自动生成的投稿 PR，检查 `SKILL.md`、`skill.json` 和 `index/skills.json`。
6. 按第 3.4 节完成审核和发布。

自动化会核验 Issue 作者权限。无写权限账号不能冒用 `internal-proxy`。

详细要求见 [内部代投稿指南](internal-proxy-submission.md)。

### 3.3 本地 Skill 包投稿

已经整理成标准目录的 Skill，可以使用仓库内置的 `submit-skills`。

先预览：

```bash
python skills/library-tools/submit-skills/scripts/submit_skills.py \
  --source <skill目录> \
  --repo-dir . \
  --author <作者署名> \
  --github <GitHub用户名> \
  --dry-run
```

确认后创建分支和 Draft PR：

```bash
python skills/library-tools/submit-skills/scripts/submit_skills.py \
  --source <skill目录> \
  --repo-dir . \
  --author <作者署名> \
  --github <GitHub用户名> \
  --push \
  --create-pr
```

该工具属于内部维护通道，不替代外部 Issue 投稿入口。

### 3.4 审核、合并与发布

维护者审核内部或外部投稿生成的投稿 PR：

1. 检查目录为 `skills/<category>/<skill-name>/`。
2. 检查 `SKILL.md` frontmatter 只包含 `name` 和 `description`。
3. 检查名称、分类、目录、来源、署名和投稿方式正确。
4. 检查步骤可复现、Prompt 可复制、案例可信且内容不重复。
5. 检查隐私、版权、安全和公开风险。
6. 正式发布前将 `skill.json.status` 改为 `reviewed`。
7. 刷新索引并运行本地校验。
8. 等待 `Validate repository / validate` 通过。
9. 如 PR 仍为 Draft，先标记为 Ready for review，然后合并到 `main`。
10. 等待 GitHub Pages 部署，搜索新 Skill 并测试目录与复制按钮。

本地合并前检查：

```bash
python scripts/ingest_issue.py --rebuild-index
python scripts/validate_skills.py
python -m unittest discover -s tests -p "test_*.py"
git diff --check
git diff --exit-code index/skills.json
```

结构校验通过只说明文件格式合格，不能替代人工内容审核。完整标准见 [Skill 审核指南](review-guide.md)。

## 4. 状态与权限规则

### Skill 状态

| 状态 | 含义 | 是否默认对外展示 |
| --- | --- | --- |
| `draft` | 自动生成、仍待补充或暂不推荐 | 否 |
| `reviewed` | 已完成结构、内容和公开合规检查 | 是 |

### 权限边界

- 外部成员可以创建 Issue，但不能直接合并或向 `main` push。
- 内部代投稿入口只接受具有写权限的账号。
- `main` 必须通过 Pull Request 修改。
- 必需 CI 为 `Validate repository / validate`。
- 单人维护时 Required approvals 可设为 `0`，但仍保留 PR、CI、禁止强推和禁止删除规则。

## 5. 常见异常处理

| 现象 | 优先检查 | 处理方式 |
| --- | --- | --- |
| Issue 后 Action 未运行 | 标题是否以 `[Skill]` 开头 | 修改标题或由维护者手动触发 |
| 解析字段失败 | 是否使用 `### 字段名`，核心字段是否齐全 | 编辑原 Issue 后重新运行 |
| 英文 ID 失败 | 是否为小写字母、数字和连字符；是否包含保留词 | 修改 ID，不静默改名 |
| 分类失败 | 是否使用仓库支持的分类名称 | 改为 `AI Shock`、`AI + 专业方法论` 或 `整活 Skill` |
| 首次外部投稿等待审批 | GitHub 首次贡献者安全机制 | 维护者核查 Issue 后批准 workflow |
| CI 通过但不能合并 | PR 仍是 Draft、分支规则或内容审核未完成 | 标记 Ready，检查规则和审核项 |
| Pages 搜不到新 Skill | PR 未合并、状态仍为 `draft`、部署未完成或索引未刷新 | 先确认 PR 已合并，再检查 `reviewed`、Actions 和索引 |
| 同名 Skill 冲突 | 已存在相同英文 ID | 人工判断合并、改名或关闭重复投稿 |

编辑原 Issue 时，系统应更新同一分支和同一投稿 PR，不应重复创建 PR。若该 Issue 对应投稿 PR 已经合并，重新运行工作流只更新 Issue 状态评论，不再创建重复 PR。

## 6. 完成标准

### 外部取用完成

- 找到适合任务且状态为 `reviewed` 的 Skill。
- 安装了完整目录。
- 客户端重新加载后能触发 Skill。

### 外部投稿完成

- Issue 创建成功。
- Action 自动运行或已获维护者批准。
- 投稿 PR 已生成，且 Issue 下能看到 PR 链接评论。
- 维护者已给出收录、补充或关闭结论。

### 内部发布完成

- 来源、署名、授权和公开风险已确认。
- `SKILL.md`、`skill.json` 和索引正确。
- `skill.json.status` 为 `reviewed`。
- 必需 CI 通过并合并到 `main`。
- GitHub Pages 可以搜索和取用该 Skill。

## 7. 相关文档

- [内部运营说明](internal-operations.md)
- [内部代投稿指南](internal-proxy-submission.md)
- [外部 Agent 投稿指南](external-agent-submission.md)
- [外部成员检索与取用指南](external-skill-usage.md)
- [Skill 审核指南](review-guide.md)
- [双入口端到端测试清单](e2e-test-checklist.md)
- [分支保护建议](branch-protection.md)
