# 内部代投稿指南

## 适用范围

此流程供拥有仓库 `write`、`maintain` 或 `admin` 权限的莞客松内部成员使用。适用于活动、围炉会、社群和项目中已经完成初筛与整理的素材。

## 素材收集

可从微信群、飞书、活动、围炉会、访谈、社群讨论和真实项目复盘中收集。建议素材表至少包含：

```text
编号、收集日期、标题、分类、原始提供者、素材来源、公开署名、
适用场景、原始内容、整理后步骤、Prompt 示例、案例效果、
风险备注、整理负责人、当前状态、对应 Issue、对应 PR
```

## 提交前

确认以下内容：

1. 有明确适用场景和可执行步骤。
2. 已搜索现有 Skill，避免重复。
3. 原始提供者、素材来源和公开署名可追溯。
4. 隐私、版权、安全和公开风险已检查。
5. 不确定信息标记为“需进一步核查”，不猜测补全。

值得入库的内容应能被他人复用、有真实效果或可信案例，并符合莞客松青年 AI 应用实践定位。只有一句想法、无法复现、依赖内部机密、明显违规或与现有 Skill 高度重复的内容暂不收录。

## 整理成 Skill

1. 选定最合适的分类。
2. 把零散经验改写成明确场景、输入、步骤和输出。
3. Prompt 中写清变量、约束和预期格式；没有 Prompt 时提供可执行流程。
4. 删除个人隐私和无权公开的信息。
5. 保留原始提供者和素材来源，不把代投稿人写成原创者。
6. 搜索 `skills/` 与 `index/skills.json`，确认不是简单重复。

## Issue 代投稿

1. 进入 `Issues → New issue → 内部 Skill 代投稿`。
2. 完整填写来源、整理人、场景、步骤和案例。
3. `投稿方式` 选择 `internal-proxy`。
4. 提交后等待 `Skill submission to PR` 生成 Draft PR。
5. 按 [审核指南](review-guide.md) 修改生成内容。
6. 可发布时将 `skill.json.status` 改为 `reviewed`。
7. 确认 `Validate repository / validate` 通过后合并。

自动化会核验 Issue 作者的仓库权限。没有内部写权限的账号不能冒用 `internal-proxy`。

## 检查 Actions 与 Draft PR

1. 在 Issue 的时间线或 `Actions` 页面确认 `Skill submission to PR` 已运行。
2. 失败时先看错误是否属于缺字段、无效分类、英文 ID 或权限问题。
3. 修正字段时编辑原 Issue；系统应更新同一分支和同一 Draft PR。
4. 在 Draft PR 中检查 Files changed、来源字段、生成目录和索引。
5. 运行 [审核指南](review-guide.md) 中的本地命令，并等待必需 CI。

满足以下条件才合并：内容可复用、来源与授权清楚、公开风险可接受、`status` 已改为 `reviewed`、索引同步且 CI 通过。

出现以下情况应关闭或退回：明显重复、广告或无关内容、无法验证来源、拒绝补充关键步骤、包含不能公开的信息，或经过修改仍不符合 Agent Skill 结构。

## 本地 Skill 包代投稿

已整理成标准目录的 Skill 可以使用仓库内置 `submit-skills`：

```bash
python skills/library-tools/submit-skills/scripts/submit_skills.py \
  --source <skill目录> \
  --repo-dir . \
  --author <作者署名> \
  --github <GitHub用户名> \
  --dry-run
```

确认预览后再创建分支和 Draft PR：

```bash
python skills/library-tools/submit-skills/scripts/submit_skills.py \
  --source <skill目录> \
  --repo-dir . \
  --author <作者署名> \
  --github <GitHub用户名> \
  --push \
  --create-pr
```

本地工具是内部维护通道，不替代外部 Issue 投稿入口。

## 交付物

- 标准 Skill 目录。
- `SKILL.md` 与 `skill.json`。
- 已更新的 `index/skills.json`。
- 关联原 Issue 的 Draft PR。
- 通过的仓库校验。

## 异常升级

- 自动化失败：先查看 Action 日志；字段问题编辑原 Issue 后重试。
- 来源或授权不清：保持 `draft`，标记“需进一步核查”，交给负责人确认。
- 疑似重复：暂停合并，在 PR 中链接已有 Skill。
- 高风险或明显不适合公开：关闭 Issue 和 PR，并记录原因。

## 测试投稿

测试标题加 `[TEST]`，正文和来源明确标注“仅用于工作流测试”。验证完成后关闭 Issue 和 Draft PR、删除生成分支，确认 `main` 与正式索引没有测试 Skill。完整步骤见 [端到端测试清单](e2e-test-checklist.md)。
