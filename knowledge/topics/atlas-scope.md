+++
id = "atlas-scope"
kind = "topic"
title = "Atlas scope, current limits, and unknowns"
summary = "Atlas is currently a Git-backed static knowledge site, without a server, online editing, issue sync, or multi-repository ingestion."
claim_status = "source-verified"
parent = "atlas-system"
sources = ["README.md", "atlas.toml", ".github/workflows/validate-and-package.yml", "tools/atlas.py"]
+++

## What exists in this bootstrap

Atlas currently has a Git-backed set of Markdown records, a small TOML vocabulary, a Python validator and static-site builder, generated HTML and JSON, browser search with type filters, a directed Connections view, tests, and a GitHub Actions build-and-package workflow. The site includes a home entrypoint, Search, Connections, Timeline, a separate system reference, an archive, and record-detail pages.

## What does not exist yet

Atlas is **not a server**. It has no database, account system, online editing, discussion/forum, issue synchronization, multi-repository ingestion, semantic search service, or automated commit-to-knowledge interpretation. Connections is a filterable list of authored graph edges, not a spatial graph renderer; relation vocabulary and semantics remain open. The current timeline has only the dated events authored as Atlas records; the preserved audit diagram is not itself a normalized event dataset.

The preserved audit bundle is a read-only historical snapshot for review. It is not silently imported as canon. Broader product knowledge, organizational history, and future plans need to be reconciled and authored deliberately.

## Questions deliberately left open

The exact record vocabulary, relation typing, hierarchy rules, source-evidence semantics, timeline depth and paging, generated site navigation, and future ingestion workflow are not fully settled. The site should make these gaps visible rather than make the bootstrap appear complete.
