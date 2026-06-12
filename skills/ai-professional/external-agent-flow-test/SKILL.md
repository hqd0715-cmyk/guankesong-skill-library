---
name: "external-agent-flow-test"
description: "Claude Code 外部投稿流程验证。用于用于验证无仓库写权限的外部成员能否通过 Claude Code 创建标准 Skill 投稿 Issue,并触发仓库自动生成 Draft PR。。关键词：Claude Code, 外部投稿, 自动化测试。Use when the user asks for this workflow, prompt pattern, or reusable AI skill."
---

# Claude Code 外部投稿流程验证

## 适用场景

用于验证无仓库写权限的外部成员能否通过 Claude Code 创建标准 Skill 投稿 Issue,并触发仓库自动生成 Draft PR。

## 使用步骤

1. 外部测试者向 Claude Code 提供投稿内容。
2. Claude Code 将内容整理为标准 Markdown Issue。
3. Claude Code 使用 GitHub CLI 创建 Issue。
4. 仓库 Actions 自动解析 Issue。
5. 系统生成 Skill 包和 Draft PR。
6. 维护者检查后关闭测试 Issue 和 PR。

## Prompt 示例

请将以下 AI 使用经验整理成莞客松 Skill 共创库的标准投稿格式。

## 注意事项

这是外部 Claude Code 投稿流程测试,不得合并到正式 Skill 库。

## 案例

外部测试者通过 Claude Code 创建 Issue,仓库自动生成 Draft PR。
