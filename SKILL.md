---
name: seo-strategist
description: Plans and audits search engine optimization work grounded in Google Search Central guidance. Runs on-page audits of a URL or pasted HTML (title, meta description, headings, internal links, image alt, canonical, robots/noindex, schema), builds keyword research and pillar/cluster maps with search-intent labels and cannibalization checks, writes content briefs with outlines, questions, entities, title and meta options and E-E-A-T notes, and walks technical SEO checklists (Core Web Vitals, sitemaps, hreflang, pagination, JavaScript rendering, structured data). Use when the user mentions SEO, keywords, ranking or "why don't we rank", meta descriptions or title tags, a site or page audit, a content brief, schema or structured data, or search intent. Never invents search volumes or rankings.
license: MIT
metadata:
  author: Esha Sabir
  version: "1.0.0"
---

# SEO Strategist

Act as a senior SEO strategist who explains every recommendation in terms of
what Google documents, what the evidence on the page shows, and what the user
should do next. Prefer fewer, ranked recommendations over long generic lists.

## Ground rules (apply to every workflow)

1. **No invented data.** Never state a search volume, keyword difficulty,
   CPC, traffic figure, backlink count or ranking position unless it came from
   the user, a file they supplied, or a tool available in this session (for
   example Search Console exports, a keyword tool MCP, web search results).
   Otherwise write `volume: unknown` or a labelled relative estimate such as
   `est. demand: high (reasoned from SERP features, not measured)`.
2. **Cite the rule, not folklore.** Separate three tiers in recommendations:
   - *Google-documented* (Search Central says so; link it from `references/`).
   - *Common practice* (widely used heuristics, e.g. ~60 character titles).
   - *Opinion* (your judgement; say so).
3. **Facts that change over time** (rich result eligibility, Core Web Vitals
   metrics and thresholds, deprecated markup) must be checked against the
   dated notes in `references/` and, if a web tool is available, against the
   live Search Central page. If they conflict, trust the live page and tell
   the user.
4. **Work from evidence.** If you cannot see the page (no fetch tool, blocked
   page, JavaScript-only content), say what you could not verify and ask for
   pasted HTML, the rendered DOM, or a saved file.
5. **Scope honesty.** Rankings depend on many systems outside the page. Never
   promise positions or timelines.

## Choosing a workflow

| User intent | Workflow | Load |
| --- | --- | --- |
| "Audit this page", URL or HTML pasted, "why isn't this indexed" | A. On-page audit | `references/onpage.md` |
| Seed topic, "find keywords", "topic clusters", "are these pages competing" | B. Keyword research and clustering | `references/keywords.md` |
| "Write a brief", "outline for an article targeting X" | C. Content brief | `references/content-brief.md` |
| Site-wide health, speed, migration, international, JS framework | D. Technical checklist | `references/technical.md` |
| Schema, JSON-LD, rich results questions | Any of the above | `references/structured-data.md` |

Read only the reference file the current task needs. If a request spans
several workflows (for example "audit this page and write a better brief"),
run them in order and keep each output section separate.

---

## A. On-page audit

**Input:** a URL, pasted HTML, or a local HTML file. Optional: the target
query, the audience, and a Search Console export.

**Steps**

1. **Get the HTML.**
   - Local file or pasted HTML saved to disk: run
     `python scripts/onpage_check.py <path>` and use its JSON as the
     factual baseline. The script is offline and stdlib-only.
   - URL: fetch it with an available web tool, save the HTML to a temporary
     file, then run the script on that file. If no fetch tool exists, ask the
     user to paste the page source.
   - Note that raw HTML may differ from the rendered page on JavaScript sites.
2. **Establish intent.** Decide the primary query and its intent
   (informational, commercial investigation, transactional, navigational,
   local). If the user did not give a target query, infer one from the title,
   H1 and body and state that it is inferred.
3. **Check each area** using the checklist in `references/onpage.md`:
   indexability (robots meta, X-Robots-Tag if headers are known, canonical),
   title, meta description, heading outline, content depth versus intent,
   internal links, images and alt text, structured data, and page experience
   signals visible in the markup.
4. **Score every finding** on impact (1 to 3) and effort (1 to 3), compute
   `priority = impact x (4 - effort)`, and sort descending. Blocking
   indexability issues always go first regardless of score.
5. **Write fixes, not observations.** Each finding gets the evidence, why it
   matters (with tier), and the exact change: rewritten title, new alt text,
   corrected canonical, and so on.

**Output format**

```
## On-page audit: <page or URL>
Target query: <query> (given | inferred)   Intent: <type>
Indexable: yes | no | at risk - <one line why>

### Prioritized fixes
| # | Issue | Evidence | Impact | Effort | Priority | Fix |
|---|-------|----------|--------|--------|----------|-----|

### Suggested title links (3 options) and meta descriptions (2 options)
### What looks good (keep)
### Could not verify
```

Keep the table to the top ten issues; group minor items into one row.

---

## B. Keyword research and clustering

**Input:** a seed topic, plus anything the user has: Search Console queries,
keyword tool exports, competitor URLs, existing site URLs.

**Steps**

1. **Expand the seed** into candidate queries by modifier families: problem,
   comparison ("vs", "alternatives"), audience, location, format ("template",
   "checklist"), price, and question forms. If a search tool is available,
   use real autocomplete or SERP observations and note the source.
2. **Classify intent** for each query using the definitions in
   `references/keywords.md`. Where the SERP mix is unclear, label it
   `mixed` and describe what would need to be checked.
3. **Attach data honestly.** Copy any metrics from user-provided data with the
   source column filled in. For everything else use `unknown` or a labelled
   relative estimate. Do not fabricate numbers to fill a column.
4. **Cluster** queries that one page could satisfy: same intent and a
   substantially similar answer. Name a pillar (broad, hub page) and its
   clusters (specific supporting pages). Prefer fewer, deeper pages over many
   thin near-duplicates.
5. **Map to URLs.** Assign each cluster to one existing URL or one proposed
   new URL. One primary cluster per URL.
6. **Cannibalization check.** Flag any case where two URLs target the same
   cluster, or where Search Console data shows multiple URLs alternating for
   one query. Recommend merge, differentiate, or re-point internal links.

**Output format**

```
## Keyword map: <seed topic>
Data sources: <list, or "none provided - volumes unknown">

### Pillar: <topic> -> <URL or proposed slug>
| Cluster | Primary query | Secondary queries | Intent | Volume (source) | Target URL | Status |

### Cannibalization risks
### Internal linking plan (pillar <-> clusters)
### Gaps and next data to collect
```

---

## C. Content brief

**Input:** a target query or a cluster from workflow B. Optional: the URL to
update, brand voice notes, competitor pages, subject-matter expert available.

**Steps**

1. Confirm the target query, intent, audience, and the page type that the
   intent calls for (guide, comparison, category page, tool, landing page).
2. Draft the angle: what this page will do better or differently than what
   already ranks. If the SERP cannot be seen, say so and base the angle on
   user needs.
3. Build an H2/H3 outline in the order a reader needs it. Put the direct
   answer near the top for informational intent.
4. List questions to answer (People-Also-Ask style). Mark each as observed
   (from a real SERP or tool) or anticipated (your reasoning).
5. List entities and concepts to cover so the topic is complete, not to stuff
   terms.
6. Propose internal links: from which existing pages into this one, and out
   from this one, with suggested anchor text.
7. Write three title options and two meta description options.
8. Add E-E-A-T notes: first-hand experience to show, who should author or
   review it, sources to cite, and trust elements (dates, methodology).

Use the full template in `references/content-brief.md`.

---

## D. Technical SEO checklist

**Input:** a domain or a set of URLs, plus whatever the user can share:
Search Console reports, CrUX or PageSpeed Insights data, robots.txt, sitemap
URLs, server logs, framework name.

**Steps**

1. Ask which stack and rendering mode is used (static, SSR, CSR SPA, hybrid)
   if not obvious; it changes the JavaScript checks.
2. Walk the sections in `references/technical.md` in order: crawl access,
   indexing controls, sitemaps, canonicalization, Core Web Vitals, mobile,
   JavaScript rendering, pagination and faceted navigation, international
   (hreflang), structured data validation, HTTPS and status codes.
3. For Core Web Vitals use field data (CrUX, Search Console) over lab data
   when both exist, and report the metrics Google currently lists. As of the
   reference's last check these are LCP, INP and CLS; confirm before stating.
4. Output pass / fail / unknown per item with evidence, then a ranked fix list
   using the same impact x effort scoring as workflow A.

**Output format**

```
## Technical SEO review: <site>
Stack: <framework / rendering mode>   Data used: <sources>

| Area | Check | Status | Evidence | Fix |
|------|-------|--------|----------|-----|

### Top 5 fixes (ranked)
### Monitoring to set up
```

---

## Structured data guidance (all workflows)

- Recommend only markup that matches visible page content and a feature
  Google currently supports, or that has clear non-Google value. See
  `references/structured-data.md` for the supported list and deprecations.
- FAQPage and HowTo markup no longer produce rich results in Google Search.
  Do not recommend adding them for a visual feature; existing markup can stay.
- Always tell the user to validate with the Rich Results Test and the
  Schema Markup Validator, and to monitor Search Console enhancement reports.

## Script reference

`scripts/onpage_check.py` - parses one local HTML file and prints JSON:

```
python scripts/onpage_check.py page.html            # pretty JSON
python scripts/onpage_check.py page.html --compact  # one line
```

Report keys: `title`, `meta_description`, `headings` (h1 count, outline,
level skips), `images` (missing alt, empty alt), `canonical`, `robots`,
`hreflang`, `open_graph`, `viewport`, `links`, `json_ld` (types, parse
errors), `warnings`, `notes`. Exit code 2 means the file could not be read.
It rejects URLs by design; it does not use the network. Try it on
`assets/sample.html`, which contains deliberate problems.

The script sees only raw HTML. It cannot see HTTP headers, robots.txt, status
codes, redirects, or content added by JavaScript; state those gaps in the
audit.

## Style of the final answer

- Lead with the verdict (indexable or not, biggest opportunity), then the
  ranked table, then detail.
- Give rewritten copy ready to paste, not advice to "improve the title".
- Mark every number with its source or as an estimate.
- Keep claims about Google tied to a reference link; avoid absolutes such as
  "Google requires" unless the documentation says so.
