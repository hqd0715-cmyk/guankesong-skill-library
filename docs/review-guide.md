# Skill 审核指南

内部成员审核内部代投或外部 Agent 投稿生成的 Draft PR 时，优先检查这几件事：

1. 结构是否标准：每个 Agent Skill 必须位于 `skills/<category>/<skill-name>/SKILL.md`。
2. frontmatter 是否干净：`SKILL.md` 只允许 `name` 和 `description`。
3. 名称是否可安装：`name` 必须使用小写字母、数字和连字符，并与目录名一致。
4. 分类是否正确：`skill.json` 中的分类应属于 AI Shock、AI + 专业方法论、整活 Skill 或库维护工具。
5. 目录是否匹配分类：AI + 专业方法论 放在 `skills/ai-professional/`，AI Shock 放在 `skills/ai-shock/`，整活 Skill 放在 `skills/fun-skills/`，库维护工具放在 `skills/library-tools/`。
6. 内容是否完整：至少包含适用场景、工作流程或使用步骤、Prompt 示例。
7. 步骤是否可复现：不要只写概念，要能照着执行。
8. Prompt 是否可直接复制：占位符、变量和输入输出要求要明确。
9. 是否存在重复：搜索 `skills/` 和 `index/skills.json`，避免同类内容重复沉淀。
10. 是否适合公开：确认没有隐私信息、内部资料、未授权搬运内容。
11. 状态是否正确：正式合并的 Skill 应将 `skill.json.status` 设为 `reviewed`；保留 `draft` 必须有明确原因。
12. 索引是否同步：重新生成 `index/skills.json` 后不应再出现未提交差异。
13. 来源是否清楚：检查 `source_provider`、`source` 和 `curator`；外部草稿缺失时应在合并前补充或明确标记。
14. 是否经过授权：公开案例不得泄露隐私，不得大段搬运未授权内容。
15. 投稿类型是否可信：`internal-proxy` 必须来自内部写权限账号；外部投稿应为 `external-claude-code`、`external-codex` 或 `external-manual`。

## PR 处理建议

- 内容基本可用：直接在 PR 中小修后合并。
- 内容方向不错但缺关键细节：由内部整理人补充或回到素材提供者核实。
- 结构不标准：由内部整理人改成标准 Agent Skill 包。
- 内容重复：关闭 PR，并在原 Issue 中贴出已有 skill 链接。
- 内容明显无关或广告：关闭 PR，并给 Issue 加 `invalid` 标签。
- 外部投稿来源不清：保持 Draft，回到原 Issue 要求补充，不因结构校验通过而直接合并。

## 合并前检查

```bash
python scripts/ingest_issue.py --rebuild-index
python scripts/validate_skills.py
python -m unittest discover -s tests -p "test_*.py"
git diff --check
git diff --exit-code index/skills.json
```

PR 的 `Validate repository` 检查必须通过。除明确保留的草稿外，应在合并前把 `skill.json.status` 从 `draft` 改为 `reviewed`。
