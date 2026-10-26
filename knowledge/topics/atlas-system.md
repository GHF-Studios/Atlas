+++
id = "atlas-system"
kind = "topic"
title = "The Atlas system"
summary = "Atlas's current authored data, graph projection, generated pages, and validation boundary, described as linked parts rather than one opaque website."
claim_status = "source-verified"
parent = "atlas"
relations = [{ type = "explains", target = "knowledge-model" }]
sources = ["atlas.toml", "tools/atlas.py", ".github/workflows/validate-and-package.yml"]
+++

## The path from source to reader

Atlas has one authoritative authored set: this Git repository. Each knowledge record is a Markdown file with TOML frontmatter. The frontmatter gives it a stable ID, one primary kind, and a claim label; optional metadata gives it a date, parent, cross-record relations, and source paths. `atlas.toml` declares the kinds and claim labels currently recognized by the validator.

The validator checks the structure it can establish mechanically: record parsing, IDs, kind placement, claim labels, dates, record references, parent cycles, and source-file existence. It cannot establish truth, owner approval, the meaning of an undocumented relation, or whether a human explanation is good.

The generator derives several read views from those records: HTML pages for orientation and browsing, a chronological view of dated events, and `atlas.json` for tools. A generated page is not a second source of truth. The JSON graph is a projection of each record's parent and relation fields, not a separately edited database.

## How to inspect a claim

Start with the record's claim label, then follow its listed sources. Site source links point at the exact Atlas Git revision used for that build when the revision is available to the builder. A passing validator only proves the checks listed above; human review is still needed for the claim itself.

## Current design boundary

This repository is the first subject Atlas explains. The current record kinds and fields are a working bootstrap, not a complete knowledge ontology. In particular, claim basis versus review state, relation vocabulary, source identity over time, and how Atlas represents present and future work still need explicit decisions. See the open questions connected to the knowledge model. The preserved audit bundle is available as evidence, but its contents have not been imported as current truth.
