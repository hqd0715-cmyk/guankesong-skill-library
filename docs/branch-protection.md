# 分支保护建议

建议在 GitHub 仓库中保护 `main` 分支：

1. 打开 `Settings`。
2. 进入 `Branches`。
3. 新建规则，Branch name pattern 填 `main`。
4. 开启 `Require a pull request before merging`。
5. 开启 `Require approvals`，建议至少 1 人审核。
6. 开启 `Dismiss stale pull request approvals when new commits are pushed`。
7. 开启 `Require status checks to pass before merging`。

外部成员不需要直接写入 `main`。默认投稿路径是 Issue 表单或 `submit-skills` 生成的审核分支，维护者审核 Draft PR 后再合并。
