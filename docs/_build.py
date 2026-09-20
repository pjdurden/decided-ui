#!/usr/bin/env python3
"""Generate the docs site from fragments in _content/.

Every page shares one shell so the nav and the sidebar cannot drift. Run
`python3 docs/_build.py` from anywhere after editing a fragment, and commit
the generated HTML alongside it.
"""
import pathlib

HERE = pathlib.Path(__file__).parent
CONTENT = HERE / "_content"

# slug, nav label, page title, one-line description
PAGES = [
    ("index",       "Overview",    "decided-ui", "The model chooses among interfaces you wrote, and you measure which one won."),
    ("concepts",    "Concepts",    "Concepts", "Slots, variants, decisions, gating: the mental model behind decided UI."),
    ("spec",        "Spec API",    "The spec API", "defineSpec, variant, presence, rank and intensity, in full."),
    ("architecture","Architecture","Architecture", "Packages, the request lifecycle, and where each piece of work happens."),
    ("jev",         "Jev",         "Jev, the decision engine", "Why a System One model rather than an LLM, and exactly what it returns."),
    ("measurement", "Measurement", "Measurement", "The Tracker contract, impression discipline, and joining conversions to variants."),
    ("comparison",  "Comparison",  "How it compares", "Against generative UI, A/B testing, feature flags and personalisation engines."),
    ("roadmap",     "Roadmap",     "Roadmap", "What exists, what is next, and what done means for each phase."),
]

SIDEBAR = [
    ("Start here", ["index", "concepts"]),
    ("Reference",  ["spec", "architecture", "jev", "measurement"]),
    ("Context",    ["comparison", "roadmap"]),
]

NAV_ORDER = [p[0] for p in PAGES]
LABEL = {p[0]: p[1] for p in PAGES}
TITLE = {p[0]: p[2] for p in PAGES}
DESC = {p[0]: p[3] for p in PAGES}


TOP = ("index", "concepts", "spec", "architecture", "jev", "measurement", "roadmap")


def href(slug):
    return "index.html" if slug == "index" else slug + ".html"


def topnav(cur):
    parts = []
    for s in NAV_ORDER:
        if s not in TOP:
            continue
        on = ' class="on"' if s == cur else ""
        parts.append('<a href="%s"%s>%s</a>' % (href(s), on, LABEL[s]))
    return "".join(parts)


def sidebar(cur):
    out = []
    for heading, slugs in SIDEBAR:
        out.append(f"<h5>{heading}</h5>")
        for s in slugs:
            on = ' class="on"' if s == cur else ""
            out.append('<a href="%s"%s>%s</a>' % (href(s), on, LABEL[s]))
    return "\n".join(out)


def page(slug, body):
    landing = slug == "index"
    shell = (
        f'<main class="wrap">{body}</main>'
        if landing
        else f'<div class="shell"><aside class="side">{sidebar(slug)}</aside>'
             f'<main class="doc">{body}</main></div>'
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE[slug]}{"" if landing else " - decided-ui"}</title>
<meta name="description" content="{DESC[slug]}">
<meta property="og:title" content="{TITLE[slug]}">
<meta property="og:description" content="{DESC[slug]}">
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="top"><div class="inner">
  <a class="brand" href="index.html">decided<span>-ui</span></a>
  <nav>{topnav(slug)}</nav>
</div></div>
{shell}
<footer><div class="inner">
  <p>decided-ui &#183; <a href="https://github.com/pjdurden/decided-ui">github.com/pjdurden/decided-ui</a>
     &#183; MIT</p>
  <p>Design and prototype. The TypeScript packages described here are not built yet.
     Decisions are made by <a href="https://typesafe.ai">Jev</a>, TypeSafe's System One model.</p>
</div></footer>
</body>
</html>
"""


def main():
    written = []
    for slug, *_ in PAGES:
        src = CONTENT / f"{slug}.html"
        if not src.exists():
            raise SystemExit(f"missing fragment: {src}")
        (HERE / f"{slug}.html").write_text(page(slug, src.read_text()), encoding="utf-8")
        written.append(slug)
    print("built:", ", ".join(written))


if __name__ == "__main__":
    main()
