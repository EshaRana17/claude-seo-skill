# seo-strategist

An open-source Agent Skill that turns Claude (or any agent that reads
`SKILL.md` skills) into a careful SEO strategist. It audits pages, builds
keyword maps, writes content briefs and runs technical SEO checklists, with
guidance grounded in Google Search Central documentation and a hard rule
against invented search volumes.

## What it does

| Workflow | You give it | You get back |
| --- | --- | --- |
| On-page audit | A URL, pasted HTML, or a saved HTML file | Indexability verdict, a prioritized fix table (impact x effort), rewritten title and meta options |
| Keyword research and clustering | A seed topic, plus any keyword or Search Console data you have | Intent-labelled queries, pillar/cluster map, URL mapping, cannibalization risks |
| Content brief | A target query or cluster | Outline with H2/H3s, questions to answer, entities, internal links, title and meta options, E-E-A-T notes |
| Technical SEO checklist | A domain, stack details, Search Console or CrUX data | Pass / fail / unknown table across crawl, indexing, sitemaps, Core Web Vitals (LCP, INP, CLS), JS rendering, pagination, hreflang, structured data |

It includes `scripts/onpage_check.py`, a standard-library Python script that
reads a local HTML file and prints a JSON report (title and meta description
lengths, H1 count, heading outline, images missing alt, canonical, robots
meta, hreflang, JSON-LD types and parse errors).

## Example prompts

- "Audit the on-page SEO of this HTML file: ./landing.html. Target query is
  'payroll software for restaurants'."
- "Here is the page source for our pricing page. Why might it not be indexed?"
- "Build a keyword cluster map for 'home composting'. Here is our Search
  Console export (queries.csv)."
- "Are /blog/best-crm and /crm-comparison cannibalizing each other?"
- "Write a content brief for 'how to choose a trail running shoe'."
- "Give me title tag and meta description options for this product page."
- "Run a technical SEO checklist for our Next.js site; here is the
  PageSpeed Insights report."
- "Which schema should a local bakery's location page use?"

## Repository layout

```
claude-seo-skill/
  SKILL.md                     skill entry point (frontmatter + workflows)
  references/
    onpage.md                  on-page audit checklist and scoring
    keywords.md                intent, clustering, cannibalization, data policy
    content-brief.md           brief template and E-E-A-T guidance
    technical.md               technical SEO checklist (CWV, sitemaps, JS, hreflang)
    structured-data.md         supported features, deprecations, JSON-LD examples
  scripts/
    onpage_check.py            offline on-page checker (stdlib only)
  assets/
    sample.html                test fixture with deliberate SEO problems
  agent.json                   manifest (no network, no env vars)
  LICENSE                      MIT
  README.md
```

## Installation

The skill's `name` is `seo-strategist`. The Agent Skills specification asks
for the skill folder to match that name, so install the contents of this
repository into a folder called `seo-strategist` (the repository folder
itself can keep any name).

### Claude Code

Personal skill, available in every project:

```bash
git clone https://github.com/EshaRana17/claude-seo-skill.git
mkdir -p ~/.claude/skills
cp -r claude-seo-skill ~/.claude/skills/seo-strategist
```

Project skill, shared with your team through version control: copy the folder
to `.claude/skills/seo-strategist/` in your repository and commit it.

Claude Code loads the skill automatically when a request matches its
description (SEO, keywords, meta description, audit, content brief, schema).
You can also invoke it directly with `/seo-strategist`.

### Claude.ai (web and desktop apps)

1. Make sure code execution is on: Settings > Capabilities > "Code execution
   and file creation" (Team plans have it on by default; Enterprise owners
   enable it, and Skills, under Organization settings).
2. Create a ZIP whose top-level folder is `seo-strategist/` containing
   `SKILL.md` and the other files.
3. Open Customize > Skills, click **+**, then **+ Create skill**, and choose
   **Upload a skill**.
4. Upload the ZIP. The skill appears in your list; toggle it on.

Menu names in Claude.ai change from time to time; if they differ, see
Anthropic's help article "Using Skills in Claude".

### Other agents that read SKILL.md

The skill follows the open Agent Skills format (https://agentskills.io): a
folder with `SKILL.md` (YAML frontmatter with `name` and `description`, then
Markdown instructions) plus optional `references/`, `scripts/` and `assets/`.
Any compatible agent can load it by placing the `seo-strategist` folder in
that agent's skills directory. Check your agent's documentation for the path.
You can validate the format with the reference validator:
`skills-ref validate ./seo-strategist`.

## Running the script yourself

Requires Python 3.8 or newer; no packages to install.

```bash
python scripts/onpage_check.py assets/sample.html
python scripts/onpage_check.py path/to/saved-page.html --compact
```

To check a live page, save its HTML first (browser "Save page as", or
`view-source:` and copy), then run the script on the file. Exit code `0`
means a report was printed; `2` means the file could not be read.

Against `assets/sample.html` it reports, among others: a 105-character title,
a 163-character meta description, two H1 elements, an H2 to H4 level skip,
two images with no alt attribute, a `javascript:` link, and FAQPage markup
(which Google no longer shows as a rich result).

## Accuracy notes

- Facts about Google Search were checked against Search Central on
  2026-11-01. Each reference file lists its sources with the documentation's
  last-updated dates. Search features change; the skill instructs the agent to
  re-verify time-sensitive facts when a web tool is available.
- Title and description length ranges in the script are display heuristics.
  Google documents no fixed character limit for either.
- The skill never fabricates search volumes, difficulty scores or rankings. It
  uses data you provide or tools available in the session, and otherwise
  labels values as unknown or as reasoned estimates.

## Security

- `scripts/onpage_check.py` reads only the local file path you pass to it. It
  makes no network requests, imports only the Python standard library, writes
  nothing to disk, and refuses URLs as input.
- The skill requires no API keys or environment variables (`agent.json`
  declares `"network": []` and `"env": []`). Any web fetching happens only
  through tools you have already enabled in your agent.
- This skill has been scanned on Vetted Agents:
  https://agentvet-seven.vercel.app/verified

## Contributing

Issues and pull requests are welcome, especially corrections when Google
updates its documentation. Please include a link to the official source for
any factual change.

## License

MIT. See `LICENSE`.
