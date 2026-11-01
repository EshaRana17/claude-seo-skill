# Keyword research and clustering reference

Detail for workflow B. The core rule: a keyword map is only as honest as its
data. Never fill a metrics column with invented numbers.

## Contents

1. Data honesty policy
2. Expanding a seed topic
3. Search intent classification
4. Clustering method
5. Pillar and cluster architecture
6. Mapping keywords to URLs
7. Cannibalization check
8. Output templates
9. Sources

---

## 1. Data honesty policy

| Situation | What to write |
| --- | --- |
| User supplied a keyword tool export | Copy the figure and name the tool and date, e.g. `1,900 (ToolX export, 2026-10)` |
| User supplied Search Console data | Use impressions, clicks, position as given; label as GSC with date range |
| A keyword or SERP tool is available in this session | Use it, cite it in the Data sources line |
| Web search only | Record observed SERP features and autocomplete phrasing; volume stays `unknown` |
| No data at all | `unknown`, optionally a relative estimate labelled as reasoning |

Relative estimate scale (only when labelled as an estimate):

- `est. high` - head term, broad, many SERP features, many commercial results.
- `est. medium` - specific but common need.
- `est. low` - long-tail, niche, or very specific phrasing.

Explain the basis in one phrase, for example "est. low - long-tail question
form". Search Console impressions are real demand signals for queries where
the site already appears; use them before any estimate.

Also avoid inventing: keyword difficulty scores, CPC, competitor traffic,
ranking positions, and "this will get N visits" forecasts.

## 2. Expanding a seed topic

Work through modifier families so coverage is systematic:

| Family | Example pattern (seed: "standing desk") |
| --- | --- |
| Definition and how-to | what is, how to, how does, setup |
| Problem / pain | back pain, wobble, too short |
| Comparison | vs, alternatives, best, top, review |
| Audience | for small spaces, for tall people, for gaming |
| Attribute | electric, manual, L-shaped, bamboo |
| Price | cheap, under 300, worth it |
| Location | near me, in [city] (only if the business is local) |
| Format | checklist, calculator, template, size chart |
| Questions | who, what, when, why, how, can, should, is |

Sources of real phrasing, in order of reliability: the site's own Search
Console queries, internal site search logs, customer support tickets and
sales calls, a keyword tool the user has, live SERP observation (autocomplete,
related searches, People Also Ask), forums and communities.

## 3. Search intent classification

Classify by what the searcher wants to accomplish, confirmed by what the
results page shows when you can see it.

| Intent | Searcher wants | Typical modifiers | Typical winning page type |
| --- | --- | --- | --- |
| Informational | To learn or solve | how, what, why, guide, ideas | Guide, tutorial, explainer |
| Commercial investigation | To compare before buying | best, vs, review, alternatives, top | Comparison, roundup, review |
| Transactional | To act now (buy, sign up, download) | buy, price, deal, coupon, order | Product, category, pricing, signup |
| Navigational | A specific site or page | brand names, "login", product names | Home page, specific product page |
| Local | A nearby provider | near me, city names, "open now" | Location page, Business Profile |

Rules:

- If a query fits two intents, label the dominant one and note the secondary,
  e.g. `commercial (some informational)`.
- If you cannot see the SERP and the phrasing is ambiguous, label `mixed` and
  list what to check.
- Intent decides page type. A transactional query rarely ranks a blog post; an
  informational query rarely ranks a category page.

## 4. Clustering method

Two queries belong in the same cluster when one page could fully satisfy both.

Signals that queries belong together (strongest first):

1. **SERP overlap:** the same URLs rank for both (if SERP data is available,
   three or more shared URLs in the top 10 is a common working threshold).
2. **Same intent and same answer:** a searcher would be satisfied by the same
   content.
3. **Lexical similarity:** shared head term with modifiers that do not change
   the answer ("standing desk height" and "how tall should a standing desk be").

Split into separate clusters when:

- Intent differs ("standing desk" transactional vs "are standing desks good
  for you" informational).
- The modifier changes the answer ("standing desk for tall people" may deserve
  its own page if the advice and products differ).
- The audience differs enough that one page would serve neither well.

Without SERP data, cluster by intent plus answer similarity and state that the
clustering is unvalidated.

## 5. Pillar and cluster architecture

- **Pillar page:** covers the broad topic, introduces each subtopic briefly, and
  links to every cluster page. Often targets the head term.
- **Cluster pages:** each targets one cluster in depth and links back to the
  pillar plus related siblings in context.
- **Commercial pages** (category, product, service) should receive internal
  links from the informational content that naturally leads to them.

Checks before proposing a new page:

- Is there an existing page that could be expanded instead?
- Is there enough distinct demand and a distinct answer to justify a new URL?
- Would the new page be thin or a near-duplicate of a sibling?

## 6. Mapping keywords to URLs

- One primary cluster per URL; secondary queries ride along.
- Map to existing URLs first. Mark status as `existing - optimize`,
  `existing - expand`, `new`, `merge into X`, or `retire/redirect`.
- Put the primary query naturally into the title, H1 and opening paragraph;
  secondary queries become H2s or answered questions where it reads well.

## 7. Cannibalization check

Cannibalization means several of your URLs compete for the same intent, so
signals split and Google may alternate between them.

How to detect:

- Two or more URLs in the map share a primary cluster.
- In Search Console, filter the query and view the Pages tab: several URLs
  receiving impressions for the same query, with the ranking URL changing over
  time.
- Titles and H1s across pages are near-identical.
- `site:` searches for the topic return several similar pages (rough check
  only).

Not every overlap is a problem: a category page and a buying guide can both
appear for a query if they serve different intents. Flag only when intent is
the same.

Remedies, in typical order of preference:

1. **Merge** the weaker page into the stronger one and 301-redirect it.
2. **Differentiate** the pages so each targets a distinct intent or modifier,
   and rewrite titles and H1s accordingly.
3. **Re-point internal links** so anchor text for the topic goes to the chosen
   page.
4. **Canonicalize** near-duplicates that must stay live (e.g. print versions).
5. `noindex` only for pages that have no search purpose.

## 8. Output templates

Keyword table:

```
| Query | Intent | Volume (source) | SERP features seen | Cluster | Target URL | Status |
|-------|--------|-----------------|--------------------|---------|------------|--------|
| standing desk height | informational | unknown | PAA, video | Desk ergonomics | /guides/standing-desk-height | new |
```

Cluster map:

```
Pillar: Standing desks -> /standing-desks (existing - expand)
  Cluster: Desk ergonomics -> /guides/standing-desk-height (new)
  Cluster: Electric vs manual -> /guides/electric-vs-manual-standing-desk (new)
  Cluster: Buying for small spaces -> /standing-desks/compact (existing - optimize)
```

Always end with "Gaps and next data to collect", for example: "Export GSC
queries containing 'standing desk' for the last 16 months to validate
demand and spot cannibalization."

## 9. Sources

- How Search works (crawling, indexing, serving):
  https://developers.google.com/search/docs/fundamentals/how-search-works
- Search Console Performance report (queries, pages, impressions):
  https://support.google.com/webmasters/answer/7576553
- Creating helpful, reliable, people-first content (last updated 2026-10-05):
  https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Spam policies (scaled content abuse, doorway pages):
  https://developers.google.com/search/docs/essentials/spam-policies
- Consolidating duplicate URLs:
  https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
