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

### Task 1: Preserve the audit and its goal as an archive

**Files:**
- Move current audit files under `archive/audit-snapshot-2026-10-26/` without content edits.
- Create `archive/audit-snapshot-2026-10-26/README.md` and `manifest.toml`.
- Add a `workstream` record that snapshots the paused audit goal and its accepted independent progress measures.

**Checks:** compare the pre/post file inventory and content hashes; ensure the snapshot note distinguishes accepted baseline from later unreconciled counts.

### Task 2: Define the bootstrap model and self-records

**Files:**
- Create `atlas.toml` and Markdown records under `knowledge/{topics,questions,decisions,evidence,events,workstreams}/`.
- Record the accepted source/derived-view boundary, the audit snapshot, and one owner-review question.

**Checks:** IDs are stable; claim status and dates are explicit; links only assert what the conversation or snapshot supports.

### Task 3: Validate and export the graph

**Files:**
- Create `tools/atlas.py` with `validate`, `build`, and `serve` commands.
- Create `tests/test_atlas.py` for duplicate IDs, missing links, parent cycles, safe rendering, and undated events.

**Checks:** run each test red before implementation, then green; run validation on all source records and inspect generated JSON.

### Task 4: Build the reviewable site

**Files:**
- Create `site/assets/style.css` and the generator templates/pages.
- Generate home, map, timeline, record pages, search index, and `atlas.json`.

**Checks:** build from a clean temporary output directory; verify every generated internal link resolves; inspect the rendered pages in a browser if available.

### Task 5: Automate and publish the preview

**Files:**
- Add GitHub Actions for validation/build and Pages deployment.
- Add a concise root README that directs readers to the generated entrypoint and explains the source/archive boundary.

**Checks:** run validation/build locally, publish to `https://ghf-studios.github.io/Atlas/`, and verify the live homepage and its first navigation links before reporting the URL.

## Completion boundary

The slice is done when the repository contains the preserved audit and goal
record, all records validate, the generated site explains itself, and its
public preview is reachable. This does not complete the larger audit or
authorize importing the remaining corpus.
