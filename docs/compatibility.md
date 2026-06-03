# Codex 与 Claude Code 兼容性说明

本库目标不是绑定某一个客户端，而是维护一组可迁移的 Agent Skill 包。默认标准采用 Codex skills 和 Claude Code skills 都能理解的最小共同结构。

## 通用结构

```text
skills/<skill-name>/
├── SKILL.md
├── skill.json
├── scripts/
├── references/
└── assets/
```

其中只有 `SKILL.md` 是运行时必需文件，`skill.json` 是本共创库用于展示、分类和审核的索引元数据。

## SKILL.md frontmatter

通用模板只允许：

```yaml
---
name: "skill-name"
description: "说明能力和触发场景。"
---
```

这样做的原因：

- Codex skill 创建规范要求 `name` 和 `description`，并建议不要把非触发字段塞进 frontmatter。
- Claude Code 可以从 `SKILL.md` 发现 skill，Claude Agent Skills 也依赖 `name` 和 `description` 做识别和触发。
- Claude Code 支持的专属字段不一定是 Codex 的通用字段，放进共创库模板会降低可迁移性。

## Claude Code 专属字段

Claude Code 支持更丰富的本地运行约束，例如工具白名单或是否禁用模型调用。投稿到本库时默认不要把这类字段写进 `SKILL.md`。如果某个 skill 必须依赖 Claude Code 专属行为，审核者应在 PR 中明确说明，并优先考虑把约束写进正文或脚本参数，而不是扩大通用模板。

## 命名约束

- 目录名必须与 `SKILL.md` 的 `name` 一致。
- 使用小写字母、数字和连字符。
- 不使用 `anthropic` 或 `claude` 作为 `name` 的组成词，避免与 Claude 平台保留词冲突。
- 中文标题可以放在正文一级标题和 `skill.json.title`，不要放进 `name`。

## 资源目录

- `scripts/`：放确定性脚本，适合整理文件、转换格式、校验结构。
- `references/`：放需要按需读取的长文档、规范或示例。
- `assets/`：放模板、图片、字体或其他输出资源。
- `agents/`：可选 UI 元数据；不是 Claude Code 或 Codex 运行 skill 的必要条件。

## 审核口径

默认入库标准是“共同子集可用”。如果投稿只能在某个平台工作，`skill.json.platforms` 可以收窄为对应平台，但 `SKILL.md` 仍应尽量保持通用结构。
