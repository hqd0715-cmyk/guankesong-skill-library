---
name: "gks-publisher-skill"
description: "莞客松推文自动化发布。用于面向需要为微信公众号文章、小红书笔记、社群运营消息、学院官号推文、活动邀约/复盘、团队叙事等多渠道批量生成中文内容的团队。特别适合已有基础 AI 工具使用经验的内容运营人员、社区运营者和技术传播者。 Skill 通过「Agent 对话式采访。关键词：wechat, content-production, agent-skill, chinese-text, ai-workflow。Use when the user asks for this workflow, prompt pattern, or reusable AI skill."
---

# 莞客松推文自动化发布

## 适用场景

面向需要为微信公众号文章、小红书笔记、社群运营消息、学院官号推文、活动邀约/复盘、团队叙事等多渠道批量生成中文内容的团队。特别适合已有基础 AI 工具使用经验的内容运营人员、社区运营者和技术传播者。

Skill 通过「Agent 对话式采访收集信息 → 识别内容配方 → 整理 brief → 生成多平台物料 → 人性化润色(集成 humanizer-zh 引擎,检测 24+ 种 AI 写作模式,5 维度评分 ≥35/50 方可通过)→ 质量检查 → 本地预览」的完整流程,确保每一条事实可追溯、不编造。

支持 7 种内容配方:tech_share(技术分享)、insight_article(认知差文章)、product_showcase(产品展示)、player_story(选手故事)、event_invitation(活动邀约)、event_recap(活动复盘)、community_call(群运营召集)。

支持 7 种发布模式:微信公众号、小红书、社群运营、学院官号、活动邀约、活动复盘、团队叙事。一次 brief 可同时输出多平台物料。

内置 6 套微信排版风格(gks_structural / gks_default / gks_elegant / gks_tech / gks_minimal / gks_teal_cream),通过自定义 Markdown 容器语法(:::callout / :::steps / :::cta / :::caption / :::hero)直接生成微信兼容的 inline-style HTML。

## 使用步骤

**方式一:Agent 对话(推荐普通团队成员使用)**

1. 对 Claude Code 或 Codex 说:「请使用 gks-publisher-skill 帮我做一份发布物料。先采访我、整理 brief,再生成 release pack 和 preview.html。不要自动发布。」
2. Agent 读取 agent_intake/ 协议,自动识别内容配方,通过每次 1-3 个问题逐步采访用户,接受零散素材粘贴。
3. Agent 识别缺失信息,生成 `briefs/projects/<slug>.md`。
4. Agent 运行 `python gks.py run --brief <brief> --recipe <recipe> --provider agent` 生成 prompt pack。
5. Agent 按 `outputs/prompts/` 中的 6 个 prompt 顺序完成 planning → writing → editing → humanizing → final check → layout。
6. Agent 运行 `python gks.py pack` 生成 release pack,`python gks.py preview` 生成 preview.html 供本地浏览器预览。
7. 确认无误后,手动复制到微信编辑器或其他平台发布。Skill 绝不自动发布。

**方式二:CLI 直接操作(适合运营负责人/开发者)**

```bash
python gks.py doctor                                    # 环境检查
python gks.py run --brief briefs/my-brief.md             # 一键生成
  --recipe event_invitation --provider none              #
  --pack --slug my-slug --channels wechat,xhs,group      #
python gks.py preview --release outputs/releases/my-slug # 本地预览
```

分步操作:

```bash
python scripts/gks_write.py --mode event_invitation --channel wechat --brief briefs/example.md
python scripts/gks_humanize.py outputs/drafts/article.md
python scripts/gks_check.py outputs/final/article.md
python scripts/gks_export.py outputs/final/article.md --format md2wechat
```

## Prompt 示例

**Agent 对话启动**

```
请使用 gks-publisher-skill 帮我做一份发布物料。先采访我、整理 brief,再生成 release pack 和 preview.html。不要自动发布。
```

**活动邀约推文**

```
请使用 gks-publisher-skill 帮我写一篇活动邀约推文。活动是 6 月 22 日晚上的 AI 围炉会,地点东莞南城。请先采访我补充细节,然后生成微信公众号推文 + 封面文案 + 群转发语 + 排版 brief。每一步都要标注事实来源。
```

**Agent 检索提示词(供 Codex / Claude Code 从库里发现本 Skill)**

```
请帮我从莞客松 Skill 共创库检索适合当前任务的 Agent Skill。
索引地址:https://raw.githubusercontent.com/hqd0715-cmyk/guankesong-skill-library/main/index/skills.json
仓库:hqd0715-cmyk/guankesong-skill-library
先读取索引,只考虑 status 为 reviewed、category 不是"库维护工具",且 platforms 包含当前客户端的 Skill。
根据我接下来描述的任务,最多推荐 3 个,并说明名称、适用理由、难度和目录。
不要立即安装;等我确认具体 Skill 后,再下载完整目录,不能只复制 SKILL.md。
我的任务是:需要为微信公众号/小红书/社群批量生成中文推文内容,包括活动邀约、活动复盘、产品展示、技术分享等多种内容类型,要求事实可追溯、不编造,并输出多平台物料包。
```

## 注意事项

1. **事实边界严格**:只使用 brief 和 knowledge/ 中的事实;不允许编造活动时间、地点、人物、奖项、合作方、报名链接、价格、名额或活动结果;缺失信息使用 `【待补充:字段名】` 标记。
2. **禁止自动发布**:Skill 只生成 Markdown 和本地预览 HTML,不接微信 API、不上传草稿箱、不自动点击"发布""群发""发送"按钮,不处理账号密码。
3. **humanizer-zh 集成**:人性化步骤依赖 humanizer-zh skill 作为核心引擎,覆盖 6 大类 24+ 种 AI 写作模式的检测与修复,输出需通过 5 维度质量评分(直接性、节奏、信任度、真实性、精炼度各 ≥8/10,总分 ≥35/50)。
4. **跨平台一致性**:一次 brief 可同时输出 wechat / xhs / group 三个渠道的物料,各渠道自动适配语气和结构。
5. **WeChat 图片处理**:SVG 和 base64 在微信编辑器粘贴时会被清除;本地预览使用 base64 嵌入方便查看,生产发布需手动上传 PNG 文件到微信素材库。
6. **环境依赖**:`pip install markdown beautifulsoup4 Pillow`。
7. **平台兼容**:已验证 Claude Code 和 Codex;Python 脚本不依赖网络,文件型知识库确保 MVP 稳定性。

## 案例

1. **AI 围炉会活动复盘**(event_recap):从零散采访素材到完整微信公众号推文 + 小红书笔记 + 群转发语 + 首图设计 brief + 排版说明 + 发布检查清单。输出目录:`outputs/releases/demo-ai-weiluhui-*/`。
2. **产品展示「牛马咖啡」**(product_showcase):使用产品展示配方生成包含产品描述、使用场景、视觉建议的完整素材包。
3. **社群运营召集**(community_call):快速生成群公告和转发文案,语气简洁、行动导向。
4. **技术分享长文**(insight_article):使用 gks_teal_cream 风格生成深度技术观察文章的微信 HTML,含黑白颗粒感首图 + 米黄底青绿点缀正文。
