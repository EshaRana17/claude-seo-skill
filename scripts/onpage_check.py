#!/usr/bin/env python3
"""onpage_check.py - offline on-page SEO inspector for a single local HTML file.

Reads one HTML file from disk and prints a JSON report describing the
signals an SEO reviewer usually checks first: title and meta description
length, H1 count, heading outline, images without alt text, canonical
link, robots directives, JSON-LD types, and basic link counts.

Design constraints:
  * Python standard library only (3.8+).
  * Never touches the network. It does not fetch URLs, follow links,
    resolve canonicals, or download JSON-LD contexts.
  * Reads only the path given on the command line.

Usage:
  python scripts/onpage_check.py path/to/page.html
  python scripts/onpage_check.py path/to/page.html --compact

Exit codes:
  0  report printed
  2  the file could not be read (missing, a directory, or unreadable)

Length thresholds in the report are heuristics, not Google rules. Google
documents no fixed character limit for titles or meta descriptions; it
truncates them to fit the device. The thresholds only flag text likely to
be cut off in a typical desktop result.
"""

import argparse
import json
import os
import sys
from html.parser import HTMLParser

# Heuristic display ranges (characters). Advisory only; see module docstring.
TITLE_RANGE = (30, 60)
DESCRIPTION_RANGE = (70, 160)

HEADING_TAGS = {"h1": 1, "h2": 2, "h3": 3, "h4": 4, "h5": 5, "h6": 6}
# Elements whose text should never be counted as visible heading/title text.
RAW_TEXT_TAGS = {"script", "style", "noscript", "template"}


def _norm(text):
    """Collapse runs of whitespace and trim."""
    return " ".join(text.split())


class PageScanner(HTMLParser):
    """Single-pass collector of on-page SEO signals."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.titles = []
        self.meta = {}  # lowercased name/property -> list of content values
        self.canonicals = []
        self.headings = []  # list of {"level": int, "text": str}
        self.images = []  # list of {"src": str, "alt": str or None}
        self.jsonld_blocks = []  # raw text of each ld+json script
        self.links = {"total": 0, "no_href": 0, "nofollow": 0,
                      "fragment_only": 0, "javascript_href": 0}
        self.hreflang = []

        self._in_title = False
        self._in_svg = 0
        self._title_buf = []
        self._heading_stack = []  # [(tag, outline entry, [text parts])]
        self._raw_depth = 0
        self._in_jsonld = False
        self._jsonld_buf = []

    # -- helpers -------------------------------------------------------
    @staticmethod
    def _attrs(attrs):
        out = {}
        for key, value in attrs:
            out[key.lower()] = "" if value is None else value
        return out

    def _add_meta(self, key, content):
        self.meta.setdefault(key.lower(), []).append(content)

    # -- parser callbacks ---------------------------------------------
    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        a = self._attrs(attrs)

        if tag == "svg":
            self._in_svg += 1
        if tag == "html" and "lang" in a:
            self.lang = a["lang"]

        if tag == "title" and not self._in_svg:
            self._in_title = True
            self._title_buf = []
        elif tag == "meta":
            content = a.get("content", "")
            if "name" in a:
                self._add_meta(a["name"], content)
            if "property" in a:
                self._add_meta(a["property"], content)
            if "http-equiv" in a and a["http-equiv"].lower() == "x-robots-tag":
                self._add_meta("x-robots-tag(meta)", content)
        elif tag == "link":
            rels = a.get("rel", "").lower().split()
            if "canonical" in rels:
                self.canonicals.append(a.get("href", ""))
            if "alternate" in rels and "hreflang" in a:
                self.hreflang.append({"hreflang": a["hreflang"],
                                      "href": a.get("href", "")})
        elif tag in HEADING_TAGS:
            # Record in document order now; text is filled in on close.
            entry = {"level": HEADING_TAGS[tag], "text": ""}
            self.headings.append(entry)
            self._heading_stack.append((tag, entry, []))
        elif tag == "img":
            self.images.append({"src": a.get("src", ""),
                                "alt": a["alt"] if "alt" in a else None})
        elif tag == "a":
            self.links["total"] += 1
            href = a.get("href")
            rel = a.get("rel", "").lower().split()
            if href is None or not href.strip():
                self.links["no_href"] += 1
            else:
                h = href.strip().lower()
                if h.startswith("#"):
                    self.links["fragment_only"] += 1
                elif h.startswith("javascript:"):
                    self.links["javascript_href"] += 1
            if "nofollow" in rel:
                self.links["nofollow"] += 1
        elif tag == "script":
            if a.get("type", "").strip().lower() == "application/ld+json":
                self._in_jsonld = True
                self._jsonld_buf = []
            else:
                self._raw_depth += 1
        elif tag in RAW_TEXT_TAGS:
            self._raw_depth += 1

    def handle_startendtag(self, tag, attrs):
        # <img/>, <meta/>, <link/> written in XHTML style.
        self.handle_starttag(tag, attrs)
        if tag.lower() in ("script", "title") or tag.lower() in HEADING_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "svg" and self._in_svg:
            self._in_svg -= 1
        if tag == "title" and self._in_title:
            self._in_title = False
            self.titles.append(_norm("".join(self._title_buf)))
        elif tag in HEADING_TAGS:
            # Close the most recent open heading of this tag.
            for i in range(len(self._heading_stack) - 1, -1, -1):
                if self._heading_stack[i][0] == tag:
                    _, entry, parts = self._heading_stack.pop(i)
                    entry["text"] = _norm("".join(parts))
                    break
        elif tag == "script":
            if self._in_jsonld:
                self._in_jsonld = False
                self.jsonld_blocks.append("".join(self._jsonld_buf))
            elif self._raw_depth:
                self._raw_depth -= 1
        elif tag in RAW_TEXT_TAGS and self._raw_depth:
            self._raw_depth -= 1

    def handle_data(self, data):
        if self._in_jsonld:
            self._jsonld_buf.append(data)
            return
        if self._raw_depth:
            return
        if self._in_title:
            self._title_buf.append(data)
        for _, _, parts in self._heading_stack:
            parts.append(data)

    def close(self):
        super().close()
        # Flush headings left open by malformed markup.
        while self._heading_stack:
            _, entry, parts = self._heading_stack.pop()
            entry["text"] = _norm("".join(parts))
            entry["unclosed"] = True


# ---------------------------------------------------------------------
# JSON-LD analysis
# ---------------------------------------------------------------------
def _collect_types(node, found):
    """Walk parsed JSON-LD and record every @type value, including nested."""
    if isinstance(node, dict):
        t = node.get("@type")
        if isinstance(t, str):
            found.append(t)
        elif isinstance(t, list):
            found.extend(str(x) for x in t)
        for value in node.values():
            _collect_types(value, found)
    elif isinstance(node, list):
        for item in node:
            _collect_types(item, found)


def analyse_jsonld(blocks):
    result = {"blocks": len(blocks), "top_level_types": [],
              "all_types": [], "errors": []}
    for index, raw in enumerate(blocks):
        text = raw.strip()
        if not text:
            result["errors"].append({"block": index, "error": "empty block"})
            continue
        try:
            data = json.loads(text)
        except ValueError as exc:
            result["errors"].append({"block": index,
                                     "error": "invalid JSON: %s" % exc})
            continue
        roots = data if isinstance(data, list) else [data]
        for root in roots:
            if not isinstance(root, dict):
                continue
            graph = root.get("@graph")
            candidates = graph if isinstance(graph, list) else [root]
            for item in candidates:
                if isinstance(item, dict):
                    t = item.get("@type")
                    if isinstance(t, list):
                        result["top_level_types"].extend(str(x) for x in t)
                    elif t:
                        result["top_level_types"].append(str(t))
        _collect_types(data, result["all_types"])
    result["all_types"] = sorted(set(result["all_types"]))
    return result


# ---------------------------------------------------------------------
# Report building
# ---------------------------------------------------------------------
def _length_status(length, low, high):
    if length == 0:
        return "missing"
    if length < low:
        return "short"
    if length > high:
        return "long"
    return "ok"


def _robots_directives(meta):
    directives = {}
    for key in ("robots", "googlebot", "googlebot-news", "x-robots-tag(meta)"):
        if key in meta:
            tokens = []
            for value in meta[key]:
                tokens.extend(t.strip().lower() for t in value.split(",")
                              if t.strip())
            directives[key] = tokens
    return directives


def build_report(path, html_text):
    scanner = PageScanner()
    scanner.feed(html_text)
    scanner.close()

    warnings = []

    # Title
    title = scanner.titles[0] if scanner.titles else ""
    title_report = {
        "text": title,
        "length": len(title),
        "status": _length_status(len(title), *TITLE_RANGE),
        "count": len(scanner.titles),
    }
    if not scanner.titles:
        warnings.append("No <title> element found.")
    elif len(scanner.titles) > 1:
        warnings.append("Multiple <title> elements (%d); browsers and "
                        "crawlers use the first." % len(scanner.titles))
    if title_report["status"] == "long":
        warnings.append("Title is %d chars; likely truncated in results "
                        "(heuristic >%d)." % (len(title), TITLE_RANGE[1]))

    # Meta description
    descs = scanner.meta.get("description", [])
    desc = _norm(descs[0]) if descs else ""
    desc_report = {
        "text": desc,
        "length": len(desc),
        "status": _length_status(len(desc), *DESCRIPTION_RANGE),
        "count": len(descs),
    }
    if not descs:
        warnings.append("No meta description; Google will build a snippet "
                        "from page text.")
    elif len(descs) > 1:
        warnings.append("Multiple meta description tags (%d)." % len(descs))
    if desc_report["status"] == "long":
        warnings.append("Meta description is %d chars; the snippet may be "
                        "cut (heuristic >%d)." % (len(desc),
                                                 DESCRIPTION_RANGE[1]))

    # Headings
    h1s = [h for h in scanner.headings if h["level"] == 1]
    if not h1s:
        warnings.append("No <h1> found.")
    elif len(h1s) > 1:
        warnings.append("%d <h1> elements; one clear main heading is easier "
                        "to interpret." % len(h1s))
    skips = []
    previous = 0
    for h in scanner.headings:
        if previous and h["level"] > previous + 1:
            skips.append("h%d -> h%d before '%s'" % (previous, h["level"],
                                                      h["text"][:60]))
        previous = h["level"]
    if skips:
        warnings.append("Heading level skips: %d (see headings.level_skips)."
                        % len(skips))
    empty_headings = sum(1 for h in scanner.headings if not h["text"])
    if empty_headings:
        warnings.append("%d empty heading element(s)." % empty_headings)

    # Images
    missing_alt = [img["src"] for img in scanner.images if img["alt"] is None]
    empty_alt = [img["src"] for img in scanner.images
                 if img["alt"] is not None and not img["alt"].strip()]
    if missing_alt:
        warnings.append("%d image(s) have no alt attribute." % len(missing_alt))

    # Canonical
    canonical_report = {
        "href": scanner.canonicals[0] if scanner.canonicals else None,
        "count": len(scanner.canonicals),
        "is_absolute": bool(scanner.canonicals) and
        scanner.canonicals[0].lower().startswith(("http://", "https://")),
    }
    if not scanner.canonicals:
        warnings.append("No rel=canonical link.")
    elif len(set(scanner.canonicals)) > 1:
        warnings.append("Conflicting canonical URLs: %s"
                        % ", ".join(sorted(set(scanner.canonicals))))
    elif not canonical_report["is_absolute"]:
        warnings.append("Canonical is relative; absolute URLs are safer.")

    # Robots
    robots = _robots_directives(scanner.meta)
    all_tokens = {t for tokens in robots.values() for t in tokens}
    noindex = "noindex" in all_tokens or "none" in all_tokens
    if noindex:
        warnings.append("Page carries noindex; it will be dropped from "
                        "Google's index once recrawled.")
    if noindex and scanner.canonicals:
        warnings.append("noindex combined with rel=canonical sends mixed "
                        "signals.")

    # JSON-LD
    jsonld = analyse_jsonld(scanner.jsonld_blocks)
    if jsonld["errors"]:
        warnings.append("%d JSON-LD block(s) failed to parse."
                        % len(jsonld["errors"]))
    deprecated_display = {"FAQPage", "HowTo"}
    shown = deprecated_display.intersection(jsonld["all_types"])
    if shown:
        warnings.append("Found %s markup; Google no longer shows these as "
                        "rich results (markup is harmless, but expect no "
                        "visual feature)." % ", ".join(sorted(shown)))

    # Other head signals
    viewport = scanner.meta.get("viewport", [])
    if not viewport:
        warnings.append("No meta viewport; check mobile rendering.")
    if not scanner.lang:
        warnings.append("No lang attribute on <html>.")

    if scanner.links["javascript_href"]:
        warnings.append("%d link(s) use javascript: hrefs, which crawlers do "
                        "not follow." % scanner.links["javascript_href"])

    return {
        "file": os.path.abspath(path),
        "bytes": len(html_text.encode("utf-8")),
        "lang": scanner.lang,
        "title": title_report,
        "meta_description": desc_report,
        "headings": {
            "h1_count": len(h1s),
            "h1_text": [h["text"] for h in h1s],
            "outline": scanner.headings,
            "level_skips": skips,
        },
        "images": {
            "total": len(scanner.images),
            "missing_alt": missing_alt,
            "empty_alt_decorative": empty_alt,
        },
        "canonical": canonical_report,
        "robots": {
            "directives": robots,
            "noindex": noindex,
            "nofollow_page": "nofollow" in all_tokens or "none" in all_tokens,
        },
        "hreflang": scanner.hreflang,
        "open_graph": {
            "og:title": (scanner.meta.get("og:title") or [None])[0],
            "og:description": (scanner.meta.get("og:description") or [None])[0],
            "og:image": (scanner.meta.get("og:image") or [None])[0],
        },
        "viewport": viewport[0] if viewport else None,
        "links": scanner.links,
        "json_ld": jsonld,
        "warnings": warnings,
        "notes": [
            "Offline check of raw HTML only: content injected by JavaScript, "
            "HTTP headers (X-Robots-Tag), robots.txt and status codes are not "
            "visible here.",
            "Length ranges are display heuristics; Google sets no fixed "
            "character limit for titles or descriptions.",
        ],
    }


def read_html(path):
    with open(path, "rb") as handle:
        raw = handle.read()
    for encoding in ("utf-8-sig", "cp1252"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Print a JSON on-page SEO report for a local HTML file "
                    "(no network access).")
    parser.add_argument("path", help="path to a local .html file")
    parser.add_argument("--compact", action="store_true",
                        help="print single-line JSON")
    args = parser.parse_args(argv)

    if "://" in args.path:
        sys.stderr.write("error: expected a local file path, not a URL. Save "
                         "the page first (e.g. view-source, Save As).\n")
        return 2
    if not os.path.isfile(args.path):
        sys.stderr.write("error: file not found: %s\n" % args.path)
        return 2
    try:
        html_text = read_html(args.path)
    except OSError as exc:
        sys.stderr.write("error: cannot read %s: %s\n" % (args.path, exc))
        return 2

    report = build_report(args.path, html_text)
    if args.compact:
        print(json.dumps(report, ensure_ascii=False, separators=(",", ":")))
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
