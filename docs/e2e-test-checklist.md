# 双入口端到端测试清单

在相关工作流合并到默认分支后执行。测试 Issue 使用明显的 `[TEST]` 标记，完成后关闭 Issue、PR，并删除生成分支。

## 内部代投稿

- [ ] 用拥有 `write` 权限的内部账号提交 `内部 Skill 代投稿` 表单。
- [ ] 确认 `submission_type` 为 `internal-proxy`。
- [ ] 确认 Action 通过权限校验。
- [ ] 确认生成 `skill-submission/issue-<编号>` 分支。
- [ ] 确认只创建一个 Draft PR。
- [ ] 确认生成的 `skill.json` 保留来源、整理人和 Issue 编号。
- [ ] 编辑原 Issue，确认原分支和原 PR 被更新。
- [ ] 用无写权限账号冒用 `internal-proxy`，确认 Action 明确失败且不创建分支。

## Claude Code 外部投稿

- [ ] 使用 [外部 Agent 投稿指南](external-agent-submission.md) 中的 Claude Code 提示词。
- [ ] 确认 Agent 只创建 Issue，没有 fork、clone、push 或创建 PR。
- [ ] 如 GitHub 对首次贡献者显示工作流审批，确认由维护者检查正文后批准。
- [ ] 确认 `submission_type` 为 `external-claude-code`。
- [ ] 确认 Draft PR 自动创建。
- [ ] 确认 Issue 作者账号写入 `skill.json.github`（表单未另填账号时）。
- [ ] 确认 `Validate repository / validate` 出现在提交检查中并通过。

## Codex 外部投稿

- [ ] 使用指南中的 Codex 提示词。
- [ ] 确认 Agent 只创建 Issue。
- [ ] 如 GitHub 对首次贡献者显示工作流审批，确认由维护者检查正文后批准。
- [ ] 确认 `submission_type` 为 `external-codex`。
- [ ] 故意省略非核心来源字段，确认生成草稿而不是脚本崩溃。
- [ ] 故意省略一个核心字段，确认 Action 给出清晰错误且不创建 PR。
- [ ] 使用无效英文 ID，确认不会被静默改名。

## 冲突与重复

- [ ] 两个 Issue 使用同一英文 ID，确认第二个目录追加 `-issue-<编号>`，不覆盖已有 Skill。
- [ ] 再次编辑同一 Issue，确认更新自己的草稿目录。
- [ ] 确认不存在同一 Issue 的重复开放 PR。

## 清理

```bash
gh issue close <issue-number> --repo hqd0715-cmyk/guankesong-skill-library
gh pr close <pr-number> --repo hqd0715-cmyk/guankesong-skill-library --delete-branch
```

清理后确认 `main`、正式索引和 GitHub Pages 未包含测试 Skill。
