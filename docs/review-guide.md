# Skill 审核指南

内部成员审核自动生成的 Draft PR 时，优先检查这几件事：

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

## PR 处理建议

- 内容基本可用：直接在 PR 中小修后合并。
- 内容方向不错但缺关键细节：评论请投稿人补充。
- 结构不标准：要求投稿人改成标准 Agent Skill 包，或由维护者迁移。
- 内容重复：关闭 PR，并在原 Issue 中贴出已有 skill 链接。
- 内容明显无关或广告：关闭 PR，并给 Issue 加 `invalid` 标签。

## 合并前检查

```bash
python scripts/ingest_issue.py --rebuild-index
python scripts/validate_skills.py
git diff --check
```

合并后可以把 `skill.json` 中的 `status` 从 `draft` 改为 `reviewed`。
