+++
id = "atlas-scope"
kind = "topic"
title = "Atlas scope, current limits, and unknowns"
summary = "Atlas is currently a Git-backed static knowledge site, without a server, online editing, issue sync, or multi-repository ingestion."
claim_status = "source-verified"
parent = "atlas"
sources = ["README.md", "atlas.toml", ".github/workflows/pages.yml", "tools/atlas.py"]
+++

## What exists in this bootstrap

Atlas currently has a Git-backed set of Markdown records, a small TOML vocabulary, a Python validator and static-site builder, generated HTML and JSON, a basic browser search, tests, and a GitHub Pages workflow. The site includes home, map, timeline, questions, archive, and record-detail views.

## What does not exist yet

Atlas is **not a server**. It has no database, account system, online editing, discussion/forum, issue synchronization, multi-repository ingestion, semantic search service, or automated commit-to-knowledge interpretation. The “map” is not yet an interactive graph renderer. The current timeline has only the dated events authored as Atlas records; the preserved audit diagram is not itself a normalized event dataset.

The preserved audit bundle is a read-only historical snapshot for review. It is not silently imported as canon. Broader product knowledge, organizational history, and future plans need to be reconciled and authored deliberately.

## Questions deliberately left open

The exact record vocabulary, relation typing, hierarchy rules, source-evidence semantics, timeline depth and paging, generated site navigation, and future ingestion workflow are not fully settled. The site should make these gaps visible rather than make the bootstrap appear complete.
