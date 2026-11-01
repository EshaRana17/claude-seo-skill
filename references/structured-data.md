# Structured data reference

Guidance for recommending, writing and validating schema.org markup for
Google Search. Supported features change often; this file records what the
Search Central gallery showed on 2026-11-01 (gallery last updated
2026-10-16). Re-check the gallery before promising any rich result.

## Contents

1. Principles
2. Features currently in Google's gallery
3. Deprecated or no longer shown
4. Choosing markup by page type
5. Writing JSON-LD well
6. Example snippets
7. Validation workflow
8. Sources

---

## 1. Principles

- **Format:** Google supports JSON-LD, Microdata and RDFa; it recommends
  JSON-LD as easiest to maintain.
- **Eligibility, not guarantee:** valid markup makes a page eligible for a rich
  result. Google decides whether to show it.
- **Match visible content:** marked-up information must be visible to users on
  the page and must not be misleading. Violations can lead to a manual action
  that removes rich result eligibility.
- **Required vs recommended properties:** missing required properties make the
  item ineligible; adding recommended properties can improve presentation.
- **Most specific type:** use the most specific applicable schema.org type and
  nest related entities (author inside Article, offers inside Product).
- **Understanding vs display:** Google says it can still use some markup to
  understand pages even when no visual feature is shown. That is not a reason
  to add markup that misrepresents a page.

## 2. Features currently in Google's gallery

As listed in the Search Central structured data gallery (checked 2026-11-01):

| Feature | Main schema.org types | Typical page |
| --- | --- | --- |
| Article | Article, NewsArticle, BlogPosting | News, blog, editorial |
| Breadcrumb | BreadcrumbList | Any page within a hierarchy |
| Carousel | ItemList (with Recipe, Course, Restaurant, Movie) | List / summary pages |
| Course list | Course, ItemList | Course catalogues |
| Dataset | Dataset | Data publishers |
| Discussion forum | DiscussionForumPosting | Forums, community threads |
| Education Q&A | Quiz | Flashcard and study pages |
| Employer aggregate rating | EmployerAggregateRating | Employer review pages |
| Event | Event | Event listings |
| Image metadata | ImageObject (creator, license) | Image-heavy pages |
| Job posting | JobPosting | Job listings |
| Local business | LocalBusiness and subtypes | Location pages |
| Math solver | MathSolver | Math tools |
| Movie carousel | Movie, ItemList | Movie lists |
| Organization | Organization | Home or about page |
| Product | Product, Offer, AggregateRating, Review | Product and merchant pages |
| Profile page | ProfilePage, Person | Author and creator profiles |
| Q&A | QAPage, Question, Answer | One question with user answers |
| Recipe | Recipe | Recipe pages |
| Review snippet | Review, AggregateRating | Reviews of supported item types |
| Software app | SoftwareApplication | App pages |
| Speakable | speakable property | News (limited availability) |
| Subscription and paywalled content | isAccessibleForFree, hasPart | Paywalled articles |
| Vacation rental | VacationRental | Rental listings |
| Video | VideoObject | Pages featuring a video |

Notes:

- Q&A (QAPage) is for pages where users submit answers to one question; it is
  not a replacement for FAQ markup on publisher-written FAQs.
- Some features are limited by region, language, or site type; check each
  feature's page before promising it.

## 3. Deprecated or no longer shown

| Feature | Status | Advice |
| --- | --- | --- |
| FAQ (FAQPage) | Google stopped showing FAQ rich results from 7 May 2026; the documentation was later removed and Search Console reporting withdrawn. Earlier (2023) it had been limited to authoritative government and health sites. | Do not add for a visual feature. Existing valid markup does no harm and can stay. Keep FAQ sections only if they help readers. |
| How-to (HowTo) | Rich results retired in 2023 (mobile, then desktop). | Do not add for a search feature. |
| Sitelinks search box | Retired in late 2024; `nositelinkssearchbox` is now ignored. | Remove from to-do lists; WebSite markup is still useful for site names. |
| Other retired features | Not listed in the 2026-10-16 gallery, including Book actions as a standalone feature, Course info, Claim review, Estimated salary, Learning video, Special announcement and Vehicle listing. | Treat as no longer producing rich results unless the live gallery says otherwise. |

When the user's site already has deprecated markup, report it as low priority
information, not as an error.

## 4. Choosing markup by page type

| Page type | Recommend | Optional / consider |
| --- | --- | --- |
| Home page | Organization (logo, url, sameAs, contact), WebSite (name, alternateName for site name) | - |
| Article / blog post | Article or BlogPosting with author (Person with url), datePublished, dateModified, image | BreadcrumbList |
| Product page | Product with Offer (price, priceCurrency, availability), Review / AggregateRating if real | Merchant listing properties (shipping, returns), BreadcrumbList |
| Category page | BreadcrumbList | ItemList only if a supported carousel applies |
| Local business location | LocalBusiness subtype with address, geo, openingHoursSpecification, telephone | Review snippet only for reviews collected on-site per policy |
| Author page | ProfilePage with mainEntity Person | - |
| Event page | Event with startDate, location, eventStatus, offers | - |
| Job page | JobPosting with datePosted, validThrough, hiringOrganization, jobLocation | - |
| Video page | VideoObject with name, thumbnailUrl, uploadDate, contentUrl or embedUrl | Key moments (Clip or SeekToAction) |
| Recipe | Recipe with image, ingredients, instructions | Video, nutrition |

Self-serving reviews: review snippets for LocalBusiness and Organization are
not shown when the business marks up reviews of itself on its own site.

## 5. Writing JSON-LD well

- Place in `<head>` or `<body>` inside
  `<script type="application/ld+json">`; multiple blocks or one `@graph` both
  work.
- Use `@id` URLs to connect entities across blocks (e.g. the Organization as
  publisher of every Article).
- Absolute URLs for `url`, `image`, `logo`, `item`.
- ISO 8601 dates with time zone where relevant (`2026-10-20T09:00:00+00:00`).
- Prices as numbers without currency symbols; currency in `priceCurrency`
  (ISO 4217).
- Keep markup generated from the same data source as the visible page so they
  cannot drift.
- If markup is injected with JavaScript, confirm it appears in the rendered
  HTML in URL Inspection.

## 6. Example snippets

Article with author and breadcrumb (one `@graph`):

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Article",
      "@id": "https://www.example.com/guides/compost#article",
      "headline": "How to Start a Compost Bin",
      "datePublished": "2026-08-02",
      "dateModified": "2026-10-11",
      "image": ["https://www.example.com/img/compost-1x1.jpg"],
      "author": {
        "@type": "Person",
        "name": "Jordan Lee",
        "url": "https://www.example.com/authors/jordan-lee"
      },
      "publisher": {"@id": "https://www.example.com/#org"}
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Guides",
         "item": "https://www.example.com/guides"},
        {"@type": "ListItem", "position": 2, "name": "Compost"}
      ]
    }
  ]
}
```

Product with offer:

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Cedar Raised Garden Bed, 4 x 8 ft",
  "image": ["https://www.example.com/img/bed-4x8.jpg"],
  "sku": "RB-48-CED",
  "brand": {"@type": "Brand", "name": "Example Garden Co"},
  "offers": {
    "@type": "Offer",
    "url": "https://www.example.com/products/raised-bed-4x8",
    "price": 189.00,
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition"
  }
}
```

Organization for the home page:

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://www.example.com/#org",
  "name": "Example Garden Co",
  "url": "https://www.example.com/",
  "logo": "https://www.example.com/img/logo-512.png",
  "sameAs": ["https://www.linkedin.com/company/example-garden-co"]
}
```

Only include `aggregateRating` or `review` when those reviews genuinely
appear on the page.

## 7. Validation workflow

1. Parse check: run `scripts/onpage_check.py` on the saved HTML; any entry in
   `json_ld.errors` is a syntax problem to fix first.
2. Rich Results Test (https://search.google.com/test/rich-results) for
   Google-supported features: fix errors, then review warnings.
3. Schema Markup Validator (https://validator.schema.org/) for general
   schema.org correctness, including types Google does not display.
4. URL Inspection in Search Console to confirm markup survives rendering.
5. After deployment, monitor the relevant Search Console enhancement report.

## 8. Sources

- Search gallery of supported features (last updated 2026-10-16):
  https://developers.google.com/search/docs/appearance/structured-data/search-gallery
- Introduction to structured data:
  https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data
- General structured data guidelines and policies:
  https://developers.google.com/search/docs/appearance/structured-data/sd-policies
- FAQ deprecation notice (FAQ rich results not shown from 2026-05-07):
  https://developers.google.com/search/docs/appearance/structured-data/faqpage
- Search Central blog announcements:
  https://developers.google.com/search/blog
- Review snippet guidelines (self-serving reviews):
  https://developers.google.com/search/docs/appearance/structured-data/review-snippet
- Site names (WebSite markup):
  https://developers.google.com/search/docs/appearance/site-names
- Rich Results Test: https://search.google.com/test/rich-results
- Schema Markup Validator: https://validator.schema.org/
- schema.org vocabulary: https://schema.org/
