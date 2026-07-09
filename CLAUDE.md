# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A collection of Akka presentation decks that are assembled from per-slide source files into self-contained HTML and published via GitHub Pages (`https://pradeeploganathan.github.io/akka-presentations/`). Each deck is a standalone Python-built static site; there is no shared framework or package manager — the build system is plain `python3` scripts with no runtime dependencies.

## Public-vs-internal rule (load-bearing)

**Everything tracked in git is served publicly by Pages, linked or not.** Direct URLs work for any committed file, and the source is visible in the public GitHub repo.

- Confidential material (working notes, RFP responses, sales enablement, positioning drafts, etc.) belongs in `/_internal/`, which is git-ignored and never published.
- Before adding any file, ask: "Am I OK with this on the public internet?" If not, it goes in `_internal/`.
- `battlecard-service-tiers-internal.html` is name-blocked in `.gitignore` because a public counterpart of the same battlecard exists — do not remove that line.

## Repo layout

```
<name>-presentation/
  slides/NN-*/           one folder per slide: slide.html / slide.css / slide.js / meta.json
  shell/                 shell.html template + shared.css + nav.js (+ kiosk.js)
  builder/build.py       assembles slides → generated/<mode>/index.html
  builder/slide-registry.json  ordered slide list; folders missing from here do NOT build
  presenters/*.json      per-presenter name/title/email/linkedin for personalized builds
  generated/             build output served by Pages (partially tracked — see per-deck .gitignore)

build-index.py           regenerates root index.html landing page
index.html               landing page (GENERATED — never hand-edit)
case-studies/            standalone case-study HTML files + case-study-rules.md
battlecard-*.{html,md,pdf}   standalone competitive briefs at repo root
```

The three decks are `sales-presentation/`, `gartner-presentation/`, and `dev-presentation/`. Gartner additionally has `builder/bundle.py` which produces a single-file HTML with images inlined as base64 data URIs.

## Build commands

All builds are `python3` (no venv, no requirements). Run from the repo root; each build script resolves paths from its own location.

```bash
# Standard build (each deck)
python3 sales-presentation/builder/build.py
python3 gartner-presentation/builder/build.py
python3 dev-presentation/builder/build.py

# Personalized (sales & gartner) — reads presenters/<name>.json
python3 sales-presentation/builder/build.py --presenter <name>

# Alternate mode — meta.json's include_in gates each slide per mode
python3 sales-presentation/builder/build.py --mode shareable   # offline screenshots
python3 sales-presentation/builder/build.py --mode live        # embedded iframe demo
python3 sales-presentation/builder/build.py --mode hands-on    # includes setup guide

# Sales "specify" variant — alternate registry + nav file
python3 sales-presentation/builder/build.py \
    --registry specify-registry.json --nav nav-specify.js \
    --out generated/specify/index.html

# Gartner single-file deck (inlines all images as data URIs)
python3 gartner-presentation/builder/bundle.py
# → gartner-presentation/generated/akka-gartner-deck.html

# Regenerate the root landing page (run AFTER rebuilding any deck)
python3 build-index.py
```

Output is always `generated/<mode>/index.html` unless `--out` overrides it. Each build also produces a `generated/akka-presentation-<mode>[-<presenter>].zip` — these zips must never be committed (per-deck `.gitignore` handles this).

## What is committed vs. built

Per-deck `.gitignore` files govern what lands in git:

| Deck | Tracked in git |
|------|----------------|
| `sales-presentation` | Only `generated/overview/` and `generated/specify/` |
| `gartner-presentation` | The full built HTML + assets (both `generated/overview/` and `generated/akka-gartner-deck.html`) |
| `dev-presentation` | Full built output except zips |

**Never blanket-ignore a presentation's published build from the root `.gitignore`** — each deck's own `.gitignore` is the source of truth, and the root file must not override it.

Any edit to slides, shell, presenter data, or assets requires a rebuild — Pages serves the committed `generated/` output, not source.

## Slide authoring rules

1. **Slide numbering** — clean sequential integers (`00`, `01`, `02`, …). No alpha suffixes (`03b-sla`). To insert a slide, renumber the sequence. An alpha-suffixed folder is a sign of an unfinished cleanup.
2. **Registry sync** — a slide folder that isn't listed in `builder/slide-registry.json` will not build, even if the folder exists. Adding or removing a slide means editing both.
3. **Slide files are fragments, not documents** — `slide.html` is an HTML fragment (no `<html>/<head>/<body>`); `slide.css` is section-scoped; `slide.js` runs against the assembled page.
4. **meta.json controls inclusion** — `include_in` gates modes; `pre_spacer` injects a black spacer before the slide; `section` (gartner only) places the slide in one of three top-rail sections.
5. **Browser-tab title** — each deck's `shell/shell.html` `<title>` must match the deck's first-slide `<h1 class="title-headline">`, formatted `<Title> — Akka`. Never copy a shell between decks without updating `<title>` — this is a common way a deck ends up showing another deck's title.
6. **Presenter substitution** — `{{PRESENTER_NAME}}`, `{{PRESENTER_TITLE}}`, `{{PRESENTER_EMAIL}}`, `{{PRESENTER_LINKEDIN}}` are the placeholders; without `--presenter` the builder strips them from output so nothing leaks as raw `{{...}}`.

## Landing page (`index.html`)

Root `index.html` is generated by `build-index.py` — **never hand-edit it**. The script:

- Reads each deck's link text from its first slide's `<h1 class="title-headline">` and kicker from `<div class="title-sub">`.
- Reads the "Last updated" date from `git log -1 --format=%cs -- <linked-file>` (falls back to `"unpublished"` for uncommitted files).
- Orders decks and battlecards latest-updated first, keyed by the last commit touching the *linked file* (finer than the displayed YYYY-MM-DD).
- Battlecards are the standalone `battlecard-*.html` files at repo root, listed in the `BATTLECARDS` array in `build-index.py`.

To add a deck or battlecard, append to the `PRESENTATIONS` or `BATTLECARDS` list at the top of `build-index.py`, re-run it, and commit `index.html`.

## Case studies

Case studies live in `case-studies/` (standalone HTML files sharing `case-study.css`) and follow strict authorial rules in `case-studies/case-study-rules.md`. Non-obvious constraints:

- **Never reference Akka libraries, actors, JVM internals, or a specific competing framework being replaced.** Speak only at the "Akka Agentic AI Platform" or "Akka Specify" umbrella level.
- Every case study must extrapolate a concrete agentic-AI use case in its final section — even for pre-AI customer stories.
- Every case study reports the same three ROI metrics: **Speed to Production**, **Cost to Operate**, **Scale**.
- No Sources section, no citation blocks, no "as reported" or "illustrative" hedges. Do the research off-page, state numbers as fact.
- Read the full rules file before writing or editing any case study. `verizon.md` / `verizon.html` is the reference implementation.

## Publishing

Pushing to `main` triggers a GitHub Pages rebuild (~30–60s). Each deck renders at `https://pradeeploganathan.github.io/akka-presentations/<path-in-repo>`. `.nojekyll` at the repo root tells Pages to serve files verbatim — do not delete it.
