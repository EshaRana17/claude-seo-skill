# On-page audit reference

Detailed checklist for workflow A. Facts were checked against Google Search
Central on 2026-11-01; the "Sources" section lists each page with the
last-updated date shown at that time. Re-check anything time-sensitive.

## Contents

1. Indexability
2. Title element and title links
3. Meta description and snippets
4. Headings and content structure
5. Content depth versus intent
6. Internal links and anchor text
7. Images
8. Canonicalization
9. Structured data on the page
10. Page experience signals visible in markup
11. Scoring and prioritization
12. Sources

---

## 1. Indexability (check first; it gates everything else)

| Check | How to verify | Failure means |
| --- | --- | --- |
| HTTP status is 200 | Header tool, browser devtools, crawler | 4xx/5xx pages drop out; soft 404s waste crawl |
| Not blocked in robots.txt | robots.txt tester / read the file | Google cannot crawl, and so cannot see on-page `noindex` either |
| No `noindex` / `none` in robots meta | `robots.directives` in script output | Page is removed from the index once recrawled |
| No `noindex` in `X-Robots-Tag` header | Response headers (script cannot see these) | Same as above; easy to miss |
| Canonical points to self or to the intended URL | `canonical.href` | Google may index a different URL |
| Content present in initial HTML or reliably rendered | Compare raw HTML to rendered DOM | Thin or empty indexed content |

Google-documented points to cite:

- Valid robots rules include `noindex`, `nofollow`, `none` (both), `nosnippet`,
  `max-snippet`, `max-image-preview`, `max-video-preview`, `notranslate`,
  `noimageindex`, `unavailable_after` and `indexifembedded`. Google ignores
  `noarchive`, `nocache` and `nositelinkssearchbox`.
- Only `googlebot` and `googlebot-news` are recognized as Google-specific
  user-agent names in the meta tag.
- If robots.txt blocks a URL, Google never sees its `noindex`. To remove a
  page from the index, keep it crawlable and serve `noindex`.
- When rules conflict, the more restrictive one applies.
- On JavaScript pages, a `noindex` in the initial HTML may stop rendering
  entirely, so removing it later with JavaScript is unreliable.

Mixed-signal patterns to flag: `noindex` plus a canonical to another URL;
canonical to a URL that redirects or 404s; page in the XML sitemap but
`noindex`.

## 2. Title element and title links

What Google says (Title links documentation):

- There is no fixed character limit for `<title>`; Google truncates the title
  link to fit the device width.
- Title links can be generated from the `<title>` element, the main visible
  title, `<h1>` and other headings, `og:title`, prominent text, anchor text
  of links to the page, and `WebSite` structured data.
- Common reasons Google rewrites titles: half-empty titles (only the brand or a
  dangling separator), obsolete titles (an old year), titles that do not
  match the page, near-identical boilerplate across many pages, no clear main
  heading, a language or script mismatch, and a repeated site name.

Practical heuristics (common practice, not Google rules):

- Lead with the words that match the query and the page's promise. Aim for
  roughly 50 to 60 characters so the important part survives truncation.
- One distinct title per URL. Put the brand at the end, short, with a single
  separator.
- Align the title and the H1. They need not be identical, but they should
  describe the same thing, otherwise Google is more likely to rewrite.
- Do not stuff variants of the keyword. Do not put a year in the title unless
  the content is genuinely updated for it.

When writing options, give three: one exact-match, one benefit-led, one that
targets a secondary modifier (for example "for beginners", "vs X").

## 3. Meta description and snippets

What Google says (Snippets documentation):

- No length limit; snippets are truncated to fit the device.
- Snippets are mostly generated from page content. A meta description is used
  when it describes the page better than on-page text for that query.
- Descriptions should be unique per page, summarize the page, and can include
  concrete details (price, author, date, specs). Programmatic descriptions are
  fine on large sites if they read naturally and vary.
- Avoid keyword lists. Controls available: `nosnippet`, `max-snippet:[n]`,
  and the `data-nosnippet` HTML attribute on specific elements.

Heuristic: about 120 to 160 characters keeps the core message visible on most
screens. Write two options: one direct summary, one that leads with a
differentiator. Never promise something the page does not deliver.

## 4. Headings and content structure

- One clear main heading (H1) helps Google and readers identify the page
  topic; multiple equally prominent headings are listed by Google as a cause
  of title rewrites. Multiple H1s are not an error in HTML, but flag them when
  they compete.
- Headings should form an outline: H2 for major sections, H3 for subsections.
  Level skips (H2 then H4) are an accessibility issue more than a ranking
  issue; report them as low impact.
- Headings should describe the section, not decorate it. Flag empty headings
  and headings used only for styling.
- For informational queries, check whether the direct answer appears early
  (in the first screen of content).

## 5. Content depth versus intent

Compare what the page offers to what the intent requires:

| Intent | The page should | Warning signs |
| --- | --- | --- |
| Informational | Answer directly, then expand with steps, examples, visuals | Long preamble; answer buried; generic advice |
| Commercial investigation | Compare options with criteria, evidence, pros and cons | One-sided, no testing details, no criteria |
| Transactional | Make the product, price, availability and next step obvious | Thin product copy, no specs, hidden price |
| Local | Show location, hours, service area, contact, reviews | No NAP details, no local proof |
| Navigational | Get the user to the destination fast | Interstitials, unclear brand |

Use Google's people-first questions as a lens: does the page add original
information or analysis, would a reader leave satisfied, is it clear who
wrote it and how? Word count is not a goal; Google lists writing to a word
count as a warning sign.

## 6. Internal links and anchor text

Google-documented:

- Google reliably follows `<a>` elements with an `href`. `javascript:` URLs
  and click handlers on non-anchor elements may not be followed.
- Anchor text should be descriptive and make sense on its own; "click here"
  is weak. For image links, the `alt` text acts as the anchor.
- Every important page should be linked from at least one other page on the
  site. No ideal number of links is given.
- Use `rel="nofollow"` sparingly, `rel="sponsored"` for paid links and
  `rel="ugc"` for user-generated links.

Audit questions:

- Is this page linked from its pillar or hub, and does it link back?
- Are there relevant sibling pages it should link to in context?
- Does the anchor text pointing to this page describe its topic?
- Are internal links nofollowed without reason? (script: `links.nofollow`)
- Are there orphaned or very deep pages (more than ~3 clicks from home is a
  common-practice warning threshold)?

## 7. Images

- Every meaningful image needs `alt` text that describes it in context.
  Decorative images should use `alt=""` so assistive tech skips them; the
  script reports these separately as `empty_alt_decorative`.
- Use descriptive file names and place images near relevant text.
- Set `width` and `height` (or CSS aspect-ratio) to prevent layout shift.
- Do not lazy-load the LCP hero image; do lazy-load below-the-fold images.
- Use modern formats and responsive `srcset` where possible.

## 8. Canonicalization

- `rel="canonical"` is a strong hint, not a directive. Google may choose a
  different canonical if other signals (redirects, sitemaps, internal links)
  disagree.
- Use absolute URLs, one canonical per page, placed in `<head>`.
- Paginated pages should each self-canonicalize; do not point page 2 to page 1.
- If JavaScript sets a canonical, it must match any canonical in the original
  HTML.
- Flag: canonical to a non-200 URL, canonical to a `noindex` URL, conflicting
  canonicals, http vs https or trailing-slash mismatches.

## 9. Structured data on the page

Use `json_ld` from the script output, then follow
`references/structured-data.md`. Key on-page checks:

- JSON parses (script reports `errors`).
- Types fit the page content and a currently supported Google feature, or
  have a clear non-Google purpose.
- Marked-up content is visible on the page.
- FAQPage and HowTo do not earn rich results in Google; do not prioritize them.

## 10. Page experience signals visible in markup

The script cannot measure performance, but the HTML reveals risks:

- Missing `meta viewport` (mobile layout problems).
- Images without dimensions (CLS risk).
- Render-blocking scripts in `<head>` without `defer` or `async`.
- Large inline scripts or many third-party tags (INP risk).
- Intrusive interstitial markup on load.
- Missing `lang` attribute (accessibility; also a language signal).

Point to `references/technical.md` for field-data checks.

## 11. Scoring and prioritization

Impact (1 to 3):

- 3: blocks indexing, wrong canonical, missing or wrong main topic signals, or
  content that does not match intent.
- 2: weak title/description, poor internal linking to an important page,
  missing alt on key images, invalid structured data for a supported feature.
- 1: heading level skips, minor duplicate tags, cosmetic issues.

Effort (1 to 3):

- 1: template or copy edit under an hour.
- 2: requires a developer change or content rewrite of a section.
- 3: architecture, migration, or new content production.

`priority = impact x (4 - effort)`; ties go to the item affecting more URLs.
Indexability blockers are listed first regardless of score.

## 12. Sources

- Title links (last updated 2025-12-10):
  https://developers.google.com/search/docs/appearance/title-link
- Snippets and meta descriptions (2026-04-20):
  https://developers.google.com/search/docs/appearance/snippet
- Robots meta tag and X-Robots-Tag (2026-03-24):
  https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag
- Link best practices (2025-12-10):
  https://developers.google.com/search/docs/crawling-indexing/links-crawlable
- Creating helpful, reliable, people-first content (2026-10-05):
  https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- JavaScript SEO basics (2026-03-04):
  https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics
- Consolidating duplicate URLs (canonicalization):
  https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- Image SEO best practices:
  https://developers.google.com/search/docs/appearance/google-images
