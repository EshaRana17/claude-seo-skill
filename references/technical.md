# Technical SEO checklist reference

Detail for workflow D. Checked against Google Search Central and web.dev on
2026-11-01. Each section lists checks, how to verify them, and the
documented rule behind them. Mark each check `pass`, `fail` or `unknown`.
Never mark `pass` without evidence.

## Contents

1. Crawl access
2. Indexing controls and status codes
3. XML sitemaps
4. Canonicalization and duplicates
5. Core Web Vitals and page experience
6. Mobile
7. JavaScript rendering
8. Pagination, infinite scroll and faceted navigation
9. International sites (hreflang)
10. Structured data validation
11. HTTPS, redirects and migrations
12. Monitoring
13. Sources

---

## 1. Crawl access

| Check | Verify with |
| --- | --- |
| robots.txt exists at the host root, returns 200, and does not block important paths, CSS or JS | Fetch `/robots.txt`; Search Console robots.txt report |
| No accidental `Disallow: /` left from staging | Read the file |
| Important pages reachable through crawlable `<a href>` links | Crawler, or inspect navigation markup |
| Server responds reliably (no spikes of 5xx or timeouts) | Search Console Crawl stats, server logs |

Remember: robots.txt controls crawling, not indexing. A blocked URL can still
be indexed from links, without content. Use `noindex` (on a crawlable URL) to
keep a page out of the index.

## 2. Indexing controls and status codes

- Search Console Page indexing report: review "Excluded by noindex",
  "Crawled - currently not indexed", "Duplicate without user-selected
  canonical", "Soft 404".
- URL Inspection: compare "Google-selected canonical" with yours, view the
  rendered HTML, and check the live test.
- Real errors return real status codes: 404/410 for gone pages, 301/308 for
  permanent moves, 503 for temporary downtime.
- Check `X-Robots-Tag` headers on HTML and non-HTML files (PDFs).

## 3. XML sitemaps

Documented rules:

- Maximum 50,000 URLs or 50 MB uncompressed per sitemap file; split larger
  sets and optionally list them in a sitemap index.
- Google uses `<lastmod>` only when it is consistently and verifiably accurate
  (the last significant change, not a trivial edit). Google ignores
  `<changefreq>` and `<priority>`.
- Submit through the Search Console Sitemaps report or API, or reference the
  sitemap with a `Sitemap:` line in robots.txt. A sitemap is a hint, not a
  guarantee.

Checks:

- Contains only canonical, indexable, 200-status URLs.
- No URLs blocked by robots.txt or marked `noindex`.
- Absolute URLs on the correct protocol and host.
- Large sites: split sitemaps by section to read indexing coverage per type.

## 4. Canonicalization and duplicates

- One preferred URL per piece of content; redirects, canonicals, internal
  links and sitemap entries all agree on it.
- Consistent protocol (https), host (www or not) and trailing-slash policy.
- Parameters for tracking, sorting and session IDs do not create indexable
  duplicates.
- `rel="canonical"` uses absolute URLs, appears once, and points to a 200,
  indexable URL.
- Compare declared vs Google-selected canonical in URL Inspection.

## 5. Core Web Vitals and page experience

Current Core Web Vitals (verify on the live pages listed in Sources before
quoting; INP replaced FID as a Core Web Vital in 2024):

| Metric | Measures | Good | Needs improvement | Poor |
| --- | --- | --- | --- | --- |
| LCP - Largest Contentful Paint | Loading | <= 2.5 s | 2.5 to 4.0 s | > 4.0 s |
| INP - Interaction to Next Paint | Responsiveness | <= 200 ms | 200 to 500 ms | > 500 ms |
| CLS - Cumulative Layout Shift | Visual stability | <= 0.1 | 0.1 to 0.25 | > 0.25 |

Assessment uses the 75th percentile of page loads, segmented by mobile and
desktop. Use field data (Chrome UX Report, Search Console Core Web Vitals
report, PageSpeed Insights field section) for status; use lab data
(Lighthouse) to diagnose.

Google states Core Web Vitals are used by its ranking systems, but good
scores do not guarantee top rankings; relevance and helpfulness dominate.
Frame CWV work as user experience plus a modest search benefit.

Common fixes by metric:

- **LCP:** serve the hero image early (no lazy-loading, `fetchpriority="high"`,
  preload if discovered late), reduce server response time, remove
  render-blocking CSS/JS, compress and size images, use a CDN.
- **INP:** break up long tasks, defer or remove heavy third-party scripts,
  reduce JavaScript executed on interaction, avoid large DOM updates, yield to
  the main thread.
- **CLS:** set width/height or aspect-ratio on images, video and embeds;
  reserve space for ads and banners; avoid inserting content above existing
  content; use `font-display` with matched fallback metrics.

Other page experience aspects Google mentions: HTTPS, no intrusive
interstitials, mobile-friendliness, and making the main content easy to
distinguish.

## 6. Mobile

- Google indexes using the mobile version of pages (mobile-first indexing).
- Content, headings, structured data, metadata and internal links should be
  equivalent on mobile and desktop.
- `meta viewport` present; tap targets usable; no content hidden behind
  interactions that Googlebot will not perform.

## 7. JavaScript rendering

Documented behaviour:

- Google processes JavaScript pages in three phases: crawling, rendering,
  indexing. Pages returning 200 are queued for rendering.
- Server-side rendering or pre-rendering is still recommended because not all
  crawlers run JavaScript.
- Google discovers links only from `<a>` elements with `href`. Use the History
  API with real paths, not `#` fragments, for client-side routing.
- `noindex` in the initial HTML may prevent rendering; do not rely on
  JavaScript to remove it.
- For SPAs, avoid soft 404s by redirecting to a URL that returns a real 404 or
  by adding `noindex` to error views.
- JavaScript may set titles and meta descriptions; a JavaScript-set canonical
  must match any canonical in the original HTML, and there should be only one.

Checks:

- Compare raw HTML (`view-source:` or `scripts/onpage_check.py` on the saved
  source) with the rendered HTML in URL Inspection. Main content, title,
  canonical, links and structured data should be present after rendering.
- Blocked JS or CSS in robots.txt that is needed for rendering.
- Content requiring clicks, scrolls or user input to load.

## 8. Pagination, infinite scroll and faceted navigation

Documented rules:

- Google no longer uses `rel="next"` and `rel="prev"`.
- Give each page in a series its own URL (e.g. `?page=2`); do not use
  fragments for page numbers.
- Link sequential pages with `<a href>`.
- Each paginated page should self-canonicalize; do not canonicalize all pages
  to page 1.
- Load-more buttons and infinite scroll need crawlable paginated URLs behind
  them, since Google does not click buttons.
- Filter and sort variations that create duplicates can be handled with
  `noindex` or by blocking crawl of those URL patterns.

Faceted navigation checks: decide which facet combinations deserve indexable
landing pages (real demand, distinct content); keep the rest out of the index
and out of the crawl where possible to save crawl budget on large sites.

## 9. International sites (hreflang)

Documented rules:

- Declare alternates with HTML `<link rel="alternate" hreflang>` tags, HTTP
  `Link` headers, or XML sitemap entries; any one method is enough.
- Every version lists itself and all other versions (the same set on every
  page), and links must be reciprocal or Google may ignore them.
- Use fully qualified URLs.
- Codes: ISO 639-1 language, optionally plus ISO 3166-1 alpha-2 region
  (`en-GB`); a region alone is invalid; `x-default` marks the fallback page.
- Locale-adaptive redirects by IP should not stop Googlebot from reaching
  each version.

Common errors: `en-UK` (should be `en-GB`), missing return links, hreflang
pointing at non-canonical or redirected URLs, and canonicals pointing every
language version to one language.

## 10. Structured data validation

- Validate with the Rich Results Test (Google features) and the Schema Markup
  Validator (general schema.org syntax).
- Monitor Search Console enhancement reports for errors and warnings.
- Confirm that marked-up content is visible and that the types are still
  supported. See `references/structured-data.md` for the current list and
  deprecations (FAQPage and HowTo no longer produce rich results).

## 11. HTTPS, redirects and migrations

- Whole site on HTTPS with valid certificates; http redirects to https.
- Avoid redirect chains and loops; update internal links to final URLs.
- Migrations: map every old URL to its best new equivalent with 301/308, keep
  redirects in place long term (Google suggests at least a year), update
  canonicals, hreflang, sitemaps and internal links, and use the Change of
  Address tool when moving domains.

## 12. Monitoring

Recommend: Search Console (Page indexing, Performance, Core Web Vitals,
enhancement reports, Crawl stats), field data via CrUX, uptime and 5xx
alerting, and a scheduled crawl to catch new noindex, canonical or
broken-link regressions after deployments.

## 13. Sources

- Core Web Vitals and Google Search (last updated 2025-12-10):
  https://developers.google.com/search/docs/appearance/core-web-vitals
- Web Vitals overview (web.dev, thresholds and 75th percentile):
  https://web.dev/articles/vitals
- Interaction to Next Paint (web.dev): https://web.dev/articles/inp
- Page experience: https://developers.google.com/search/docs/appearance/page-experience
- Build and submit a sitemap (2026-07-08):
  https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- Robots.txt introduction:
  https://developers.google.com/search/docs/crawling-indexing/robots/intro
- Robots meta tag (2026-03-24):
  https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag
- JavaScript SEO basics (2026-03-04):
  https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics
- Pagination and incremental page loading (2025-12-10):
  https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading
- Localized versions of your pages, hreflang (2026-09-21):
  https://developers.google.com/search/docs/specialty/international/localized-versions
- Mobile-first indexing best practices:
  https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing
- Site moves with URL changes:
  https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes
- Consolidating duplicate URLs:
  https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
