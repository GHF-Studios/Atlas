# Atlas Self-Description Implementation Plan

> **For agentic workers:** Use inline execution in this session; the user explicitly asked to proceed. Tasks are tracked here.

**Goal:** Publish a small self-describing Atlas site that preserves the current audit snapshot and lets Leslie review Atlas before broader knowledge is imported.

**Architecture:** Markdown records with TOML frontmatter are the editable source. A Python standard-library validator/build tool produces static HTML and `atlas.json`; GitHub Actions validates and publishes a reviewable site.

**Tech Stack:** Markdown, TOML, Python 3.11 standard library, static HTML/CSS/JavaScript, GitHub Actions and GitHub Pages preview.

**Spec:** [Atlas self-description design](../specs/2026-10-26-atlas-self-description-design.md)

## Global constraints

- GitHub is canonical; generated hosting output is replaceable.
- The topic/question/decision structure is primary; timeline is a derived event view.
- Preserve audit artifacts as an unreviewed snapshot; do not convert them to canonical claims.
- No source repositories or their files are modified.
- No broad knowledge import before owner review of the entrypoint.

## Review focus

- Invalid or duplicate record IDs and missing relation targets must fail validation.
- Parent cycles must fail rather than make navigation recurse indefinitely.
- Markdown/TOML text containing HTML must not execute in generated pages.
- A record with no date must remain visible in graph/search but not be given a fabricated timeline date.
- A Pages build must work from a fresh checkout and publish only generated output.

---

### Task 1: Preserve the audit bundle — complete

**Files:**
- Preserve the existing audit bundle under `archive/audit-snapshot-2026-10-26/`.
- Add `PRESERVATION.md` and link it from the archive guide.
- Refresh nine files from newer workspace copies while keeping the prior committed versions in Git history.

**Checks:** inventory and content comparison passed; all 28 prior bundle files remain present; the nine refreshed workspace files match byte-for-byte. Commit `874a24a` pushed to `main`.

### Task 2: Define the bootstrap model and self-records — complete

**Files:**
- Create `atlas.toml` and Markdown records under `knowledge/{topics,questions,decisions,evidence,events,workstreams}/`.
- Record Atlas, the source/derived-view boundary, the audit snapshot, one owner-review question, and the active Atlas bootstrap workstream.

**Checks:** IDs are stable; claim status and dates are explicit; links only assert what the conversation or snapshot supports.

### Task 3: Validate and export the graph — complete

**Files:**
- Create `tools/atlas.py` with `validate`, `build`, and `serve` commands.
- Create `tests/test_atlas.py` for duplicate IDs, missing links, parent cycles, safe rendering, and undated events.

**Checks:** run each test red before implementation, then green; run validation on all source records and inspect generated JSON.

### Task 4: Build the reviewable site — complete

**Files:**
- Create `site/assets/style.css` and the generator templates/pages.
- Generate home, map, timeline, record pages, search index, and `atlas.json`.

**Checks:** build from a clean temporary output directory; verify every generated internal link resolves; inspect the rendered pages in a browser if available.

### Task 5: Automate and publish the preview — in progress

**Files:**
- Add GitHub Actions for validation/build and Pages deployment.
- Add a concise root README that directs readers to the generated entrypoint and explains the source/archive boundary.

**Checks:** run validation/build locally, publish to `https://ghf-studios.github.io/Atlas/`, and verify the live homepage and its first navigation links before reporting the URL.

## Completion boundary

The slice is done when the repository contains the preserved audit and goal
record, all records validate, the generated site explains itself, and its
public preview is reachable. This does not complete the larger audit or
authorize importing the remaining corpus.
