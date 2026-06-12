# 分支保护建议

建议在 GitHub 仓库中保护 `main` 分支：

1. 打开 `Settings`。
2. 进入 `Branches`。
3. 新建 Ruleset，目标分支选择 `main`。
4. 开启 `Require a pull request before merging`。
5. 单人维护仓库将 Required approvals 设为 `0`；GitHub 不会把 PR 作者对自己的 Approve 计入有效批准。
6. 开启 `Require status checks to pass before merging`。
7. 将 `Validate repository / validate` 设为必需状态检查。
8. 开启 `Block force pushes` 和 `Restrict deletions`。

外部成员不需要 GitHub 仓库权限，也不直接 push 或创建 PR。外部 Agent 只创建标准化 Issue；系统使用仓库自身的 `GITHUB_TOKEN` 生成 Draft PR，并由内部成员审核。
