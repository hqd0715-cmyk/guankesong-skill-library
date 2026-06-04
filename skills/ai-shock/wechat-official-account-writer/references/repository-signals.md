# Repository Signals

Use this reference when a request overlaps with existing WeChat Official Account tooling and the agent needs to decide whether to stay in writing mode or hand off to another workflow.

## Observed Repository Categories

Markdown-to-WeChat formatting:
- `lyricat/wechat-format`: Converts Markdown into WeChat-specific HTML formatting.
- `geekjourneyx/md2wechat-skill`: Provides Markdown-to-WeChat formatting and publishing-oriented tooling.

Article extraction and reuse:
- `ericyangpan/wechat2markdown`: Converts WeChat Official Account articles to Markdown.
- Similar repositories often focus on scraping, metadata extraction, image download, and content archiving.

Visual content production:
- `byodian/oneimg`: Turns text into image posts suitable for long-image articles and social platforms.

Historical article or account search:
- Repositories around WeChat MP APIs often focus on searching account history, collecting article data, or managing draft/publication workflows.

## Skill Boundary

This skill should handle editorial tasks: topic ideation, angle selection, research, outline, drafting, rewriting, title options, summaries, and final quality review.

Do not merge formatting, scraping, publishing, or image-generation workflows into this skill unless the user explicitly asks for a writing deliverable that must be prepared for one of those tools. In that case, output clean Markdown and concise production notes instead of pretending to operate the external tool.
