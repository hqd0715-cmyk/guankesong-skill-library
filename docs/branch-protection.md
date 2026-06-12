# 分支保护建议

建议在 GitHub 仓库中保护 `main` 分支：

1. 打开 `Settings`。
2. 进入 `Branches`。
3. 新建规则，Branch name pattern 填 `main`。
4. 开启 `Require a pull request before merging`。
5. 开启 `Require approvals`，建议至少 1 人审核。
6. 开启 `Dismiss stale pull request approvals when new commits are pushed`。
7. 开启 `Require status checks to pass before merging`。
8. 将 `Validate repository / validate` 设为必需状态检查。

外部成员不需要 GitHub 仓库权限，也不直接通过 GitHub 投稿。默认流程是团队收集素材，由拥有写入权限的内部成员代填 Issue 表单，系统生成 Draft PR 后再由内部成员审核。
