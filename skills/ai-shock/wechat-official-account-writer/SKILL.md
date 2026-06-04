---
name: wechat-official-account-writer
description: "Plan, research, draft, revise, and quality-check Chinese WeChat Official Account articles. Use when the user asks to write, rewrite, polish, outline, title, localize, or prepare a 微信公众号/公众号推文 article, including topic ideation, angle selection, source research, mobile-readable structure, title hooks, summaries, calls to action, and final editorial review."
---

# WeChat Official Account Writer

Use this skill to produce publication-ready Chinese WeChat Official Account articles from a topic, rough notes, pasted material, interview transcript, product brief, event brief, or existing draft.

## Workflow

1. Clarify the audience, goal, topic boundary, publishing context, and desired voice from the user request. If any of these are missing, infer conservative defaults and state them briefly.
2. Classify the article type: insight/opinion, explainer, practical guide, product or tool review, case study, event recap, brand announcement, interview/profile, or conversion article.
3. For current, factual, product, legal, policy, financial, medical, or technical claims, research and verify with reliable sources before drafting. Read `references/research-and-fact-check.md` when source quality or recency matters.
4. Choose one sharp angle and build a mobile-first outline. Read `references/article-patterns.md` when selecting a structure, title pattern, opening, section rhythm, or ending.
5. Draft in Chinese unless the user asks otherwise. Prefer short paragraphs, concrete examples, clear section headings, and transitions that keep the reader moving.
6. Revise for platform fit: remove generic AI phrasing, tighten claims, improve the title and deck, check source attribution, and ensure the ending matches the goal.
7. Deliver the final article plus optional title candidates, summary/摘要, cover-image direction, and publishing notes only when useful.

## Output Defaults

- Produce the article body in Markdown.
- Provide 3-8 title candidates when the user asks for title help or when the initial title is weak.
- Include a short 摘要 only when the user asks for publishing-ready metadata or the article is meant to be sent to the WeChat editor.
- Keep links as plain text when the destination may be pasted into WeChat.
- Avoid overusing emoji, slogan-heavy copy, exaggerated certainty, and empty motivational language.

## Scope Boundaries

- Focus on editorial work: topic selection, research, angle, outline, drafting, rewriting, title options, summary, and quality review.
- Do not promise direct WeChat publishing, account API operations, or final visual layout unless the user provides a specific tool or workflow.
- When the user asks for Markdown-to-WeChat formatting, article scraping, auto-publishing, or long-image generation, clarify that those are adjacent production tasks and either hand off to the relevant tool or provide only writing-ready Markdown.

## Drafting Rules

- Start from reader pain, curiosity, conflict, or a concrete scene. Do not open with broad historical background unless the article type requires it.
- Make one main point per section. Put the important sentence early, then support it with examples, data, steps, or contrast.
- Use specific nouns and verbs. Replace vague phrases such as "赋能", "重塑", "值得关注" with concrete outcomes.
- When adapting source material, reorganize in original language and cite or mention sources as needed. Do not closely paraphrase a single article.
- Separate facts from judgments. Mark uncertainty when evidence is incomplete.
- For service, product, event, or brand articles, make the value proposition visible in the first third of the article.

## Revision Checklist

Before finalizing, check:

- Title: specific, readable, and aligned with the article rather than clickbait.
- Opening: gives the reader a reason to continue within the first 150 Chinese characters.
- Structure: sections can be scanned on mobile and do not repeat the same point.
- Evidence: time-sensitive claims are verified; numbers have sources or are framed as estimates.
- Tone: sounds like a human editor, not a generic AI assistant.
- Ending: includes a clear takeaway, next step, question, or call to action when appropriate.

## References

- Read `references/article-patterns.md` for article types, structures, title formulas, openings, and endings.
- Read `references/research-and-fact-check.md` for research strategy, source ranking, claim verification, and citation handling.
- Read `references/repository-signals.md` when deciding whether a WeChat request belongs to writing, formatting, scraping, auto-publishing, or image-generation workflows.
