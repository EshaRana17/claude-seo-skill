# Content brief reference

Template and guidance for workflow C. A brief exists so that a writer who has
never seen the keyword research can produce a page that satisfies the intent,
earns links from the site's own pages, and shows real expertise.

## Contents

1. Before writing the brief
2. Brief template
3. Writing the outline
4. Questions to answer
5. Entities and concepts
6. Internal links
7. Title and meta options
8. E-E-A-T notes
9. Quality bar and common mistakes
10. Sources

---

## 1. Before writing the brief

Confirm or infer, and state which:

- Target query and its intent (see `references/keywords.md`).
- Page type the intent calls for (guide, comparison, category, product,
  landing page, tool).
- New page or update to an existing URL. For updates, keep the URL.
- Audience: expertise level, the job they are trying to get done, and the
  decision or action that should follow.
- What already ranks, if a SERP or search tool is available. Note patterns
  (format, depth, freshness, media) rather than copying structures.
- What the site can offer that others cannot: first-hand testing, proprietary
  data, practitioner experience, original photos, tools.

## 2. Brief template

```
# Content brief: <working title>

## Summary
Target query: <primary query>
Secondary queries: <list>
Intent: <type> - <one sentence on what the searcher needs>
Page type: <type>      URL: <existing URL or proposed slug>
Audience: <who, expertise level>
Goal / next action: <subscribe, compare, buy, contact>
Demand data: <figures with source, or "unknown">

## Angle
<2-3 sentences: what this page will do better or differently>

## Outline
H1: <main heading>
Intro: <what the first 100 words must deliver>
H2: <section>
  H3: <subsection>
  ...
H2: <section>
...
Conclusion / next step: <what it should point to>

## Questions to answer
- <question> (observed | anticipated) -> answer in <section>

## Entities and concepts to cover
- <entity> - <why it matters to the reader>

## Evidence and assets
- Original data, examples, photos, screenshots, quotes needed
- Sources to cite (primary sources preferred)

## Internal links
In (pages that should link here): <URL> - anchor: "<text>"
Out (pages this should link to): <URL> - anchor: "<text>"

## Title options
1. <option> (<n> chars)
2. ...
3. ...

## Meta description options
1. <option> (<n> chars)
2. ...

## E-E-A-T notes
Author / reviewer: <who and why qualified>
Experience to show: <first-hand elements>
Trust elements: <dates, methodology, disclosures, contact>

## Structured data
<types that fit, or "none needed">

## Out of scope
<topics to leave to other pages, to avoid cannibalization>
```

## 3. Writing the outline

- Order sections by the reader's path to their goal, not by keyword list.
- For informational intent, deliver the direct answer in the intro or first
  section, then add depth.
- For commercial investigation, state the evaluation criteria early, then
  compare against them consistently.
- For transactional pages, the brief covers product facts, objections,
  specifications, shipping/returns, and trust signals rather than a long
  article.
- H2s should be scannable on their own. A reader skimming only H2s should
  understand the page.
- Note where a table, checklist, diagram, video or calculator would serve the
  reader better than prose.
- Do not specify a word count as a goal. If the writer needs guidance, give a
  range based on what the outline requires and say it is a planning estimate.

## 4. Questions to answer

Gather questions from, in order of preference: support tickets and sales
conversations, Search Console queries phrased as questions, observed People
Also Ask and related searches, community forums, and your own reasoning.

- Label each as `observed` (seen in real data, name the source) or
  `anticipated` (reasoned).
- Map each question to the section that answers it. Questions that need
  their own page belong in "Out of scope".
- Answer each question in the first sentence of its section, then expand.

Note: FAQ sections can help readers, but FAQPage markup no longer produces
rich results in Google Search. Recommend an FAQ section only when it serves
users, not for a search feature.

## 5. Entities and concepts

Entities are the people, products, places, organizations, standards and
concepts a knowledgeable treatment would mention. They signal completeness to
readers and help search systems understand the topic.

- List 8 to 20, each with a short note on why it matters.
- Include measurable specifics (units, standards, version numbers) where
  relevant.
- Do not ask writers to repeat terms for density. Coverage, not frequency.

## 6. Internal links

- **Inbound:** list existing pages that should link to the new page, with
  natural anchor text describing its topic. The pillar page must link to it.
- **Outbound:** link to the pillar, relevant siblings, and the commercial page
  the reader is likely to need next.
- Anchors should be descriptive and readable on their own; avoid "click here"
  and avoid repeating the exact same anchor everywhere.

## 7. Title and meta options

Title options (aim for the core message in roughly the first 50 to 60
characters; this is a display heuristic, Google sets no fixed limit):

1. Exact-match: primary query plus a clear qualifier.
2. Benefit-led: the outcome the reader gets.
3. Modifier-led: targets a high-value secondary query.

Meta description options (roughly 120 to 160 characters, heuristic):

1. Direct summary of what the page covers and who it is for.
2. Differentiator first: original data, testing, tool, or unique angle.

Keep the H1 consistent with the chosen title so Google has one clear main
title. Avoid dates unless the page will be maintained.

## 8. E-E-A-T notes

E-E-A-T (experience, expertise, authoritativeness, trust) is not itself a
ranking factor, according to Google, but Google's systems use signals that
correlate with it, and trust matters most. It carries extra weight for
topics that affect health, finances, safety or well-being (YMYL).

Use Google's Who / How / Why framing:

- **Who:** a byline with a link to a real author bio; a qualified reviewer for
  YMYL topics. Never fabricate authors, credentials or headshots.
- **How:** explain methodology (how products were tested, where data came
  from) and disclose meaningful use of automation or AI where readers would
  expect it.
- **Why:** the page exists to help the reader, not to attract search visits
  for their own sake.

Concrete experience elements to request: original photos, measurements,
test results, screenshots, case studies, quotes from practitioners, and
"what we got wrong" notes.

## 9. Quality bar and common mistakes

Before handing over, check that the brief:

- States intent and page type explicitly.
- Contains no invented statistics or search volumes.
- Has an angle that is more than "cover everything competitors cover".
- Assigns each question to a section.
- Lists internal links in both directions.
- Names a qualified author or reviewer for YMYL topics.

Common mistakes: chasing a word count, copying competitor headings, stuffing
keyword variants into H2s, promising rich results from markup Google no
longer displays, and briefing a new page when an existing one should be
expanded.

## 10. Sources

- Creating helpful, reliable, people-first content (last updated 2026-10-05):
  https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Google Search's guidance about AI-generated content:
  https://developers.google.com/search/blog/2023/02/google-search-and-ai-content
- Title links (2025-12-10):
  https://developers.google.com/search/docs/appearance/title-link
- Snippets and meta descriptions (2026-04-20):
  https://developers.google.com/search/docs/appearance/snippet
- Link best practices (2025-12-10):
  https://developers.google.com/search/docs/crawling-indexing/links-crawlable
- FAQ rich result deprecation notice:
  https://developers.google.com/search/docs/appearance/structured-data/faqpage
