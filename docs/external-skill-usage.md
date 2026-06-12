# 外部成员检索与取用 Skill

## 最短路径

1. 打开 [莞客松 Skill 共创库展示页](https://hqd0715-cmyk.github.io/guankesong-skill-library/)。
2. 按任务关键词、标题、作者或标签搜索。
3. 默认结果只展示 `reviewed` 且适合外部使用的 Skill，不展示内部库维护工具。
4. 打开完整目录检查 `SKILL.md` 和附带资源。
5. 点击对应按钮，复制 Codex 或 Claude Code 取用提示词。
6. 把提示词交给本地 Agent 执行，确认后重启或重新加载客户端。

不要只下载 `SKILL.md`。Skill 可能依赖同目录中的 `scripts/`、`references/`、`assets/` 或 `agents/`。

## 不知道选哪个 Skill

复制下面的提示词交给 Codex 或 Claude Code，并补充自己的任务：

```text
请帮我从莞客松 Skill 共创库检索适合当前任务的 Agent Skill。

索引地址：
https://raw.githubusercontent.com/hqd0715-cmyk/guankesong-skill-library/main/index/skills.json

仓库：
hqd0715-cmyk/guankesong-skill-library

先读取索引，只考虑 status 为 reviewed、category 不是“库维护工具”，
且 platforms 包含当前客户端的 Skill。
根据我接下来描述的任务，最多推荐 3 个，并说明名称、适用理由、难度和目录。
不要立即安装；等我确认具体 Skill 后，再下载完整目录，不能只复制 SKILL.md。

我的任务是：<在这里填写需求>
```

## Codex 取用

确定 Skill 后，可直接告诉 Codex：

```text
请安装并验证这个 Agent Skill：

仓库：hqd0715-cmyk/guankesong-skill-library
分支：main
目录：skills/<分类目录>/<skill-name>

优先使用 Codex 内置的 skill-installer；如果不可用，再从 GitHub 下载。
必须复制整个 Skill 目录及其所有子目录，不要只复制 SKILL.md。
安装到 $CODEX_HOME/skills/<skill-name>；未设置 CODEX_HOME 时使用
~/.codex/skills/<skill-name>。
如果目标目录已存在，不要覆盖，先告诉我。
安装完成后检查 SKILL.md，并提醒我重启 Codex。
```

Codex 内置安装器可直接使用 GitHub 路径。例如：

```text
请使用 skill-installer 从
https://github.com/hqd0715-cmyk/guankesong-skill-library/tree/main/skills/ai-shock/wechat-official-account-writer
安装该 Skill。
```

## Claude Code 取用

确定 Skill 后，可直接告诉 Claude Code：

```text
请从 GitHub 安装并验证这个 Agent Skill：

仓库：hqd0715-cmyk/guankesong-skill-library
分支：main
目录：skills/<分类目录>/<skill-name>
目标目录：~/.claude/skills/<skill-name>

只下载该 Skill 的完整目录，不要为了安装一个 Skill 克隆整个仓库。
必须保留 scripts、references、assets 等子目录，不能只复制 SKILL.md。
如果目标目录已存在，不要覆盖，先告诉我。
安装完成后检查 SKILL.md，并提醒我重新加载 Claude Code。
```

项目希望共享 Skill 时，可把目标目录改为：

```text
.claude/skills/<skill-name>
```

## 安装后验证

1. 目标目录中存在 `SKILL.md`。
2. 附带资源目录没有遗漏。
3. 重启或重新加载客户端。
4. 用自然语言描述对应任务，观察 Skill 是否被触发。
5. 需要强制触发时，明确写出 Skill 名称。

发现内容问题时，请在仓库创建普通 Issue；不要直接修改或覆盖本地来源不明的 Skill。
