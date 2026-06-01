# Skill 审核指南

内部成员审核自动生成的 Draft PR 时，优先检查这几件事：

1. 分类是否正确：AI Shock、AI + 专业方法论、整活 Skill 不要混放。
2. 标题是否清楚：标题需要能被搜索到，也需要让人一眼知道用途。
3. 内容是否完整：至少包含适用场景、步骤、Prompt 示例。
4. 步骤是否可复现：不要只写概念，要能照着执行。
5. Prompt 是否可直接复制：占位符、变量和输入输出要求要明确。
6. 是否存在重复：搜索 `skills/` 和 `index/skills.json`，避免同类内容重复沉淀。
7. 是否适合公开：确认没有隐私信息、内部资料、未授权搬运内容。

## PR 处理建议

- 内容基本可用：直接在 PR 中小修后合并。
- 内容方向不错但缺关键细节：评论请投稿人补充。
- 内容重复：关闭 PR，并在原 Issue 中贴出已有 Skill 链接。
- 内容明显无关或广告：关闭 PR，并给 Issue 加 `invalid` 标签。

## 合并前检查

```bash
python scripts/ingest_issue.py --rebuild-index
git diff --check
```

合并后可以把 Skill 的 `status` 从 `draft` 改为 `reviewed`。
