# Loo-Cast / Vapor cross-product audit

This repository preserves a working audit snapshot so its scope, evidence, and open questions can be reviewed before the audit continues. It is not a product repository and makes no claim that the audit is complete.

## Read first

1. [Checkpoint and remaining work](CHECKPOINT.md)
2. [Research index](loo-cast-vapor-research-index.md)
3. [Current-state semantic cross-reference](current-state-semantic-cross-reference.md)
4. [Semantic diff review](loo-cast-vapor-semantic-diff-review.md)
5. [History timeline](loo-cast-vapor-history-timeline.md)
6. [Origin and intent reconstruction](loo-cast-vapor-origin-and-intent.md)
7. [Evidence atlas](vapor-ecosystem-evidence-atlas.md)

Focused design crosswalks: [product/workflow decisions](product-workflow-designs-crosswalk.md), [content graph](content-graph-design-crosswalk.md), [console/editor](console-editor-design-crosswalk.md), [Premium Docs](premium-docs-crosswalk.md), and [historical glossary corpus](historical-glossary-corpus-map.md).

The timeline diagram is available as [PlantUML](loo-cast-vapor-mega-timeline.puml) and [rendered SVG](loo-cast-vapor-mega-timeline.svg). The inventory and source ledgers are available in both [Markdown](latest-repository-file-inventory.md) / [CSV](latest-repository-file-inventory.csv) and [Markdown](latest-source-file-coverage.md) / [CSV](latest-source-file-coverage.csv).

## Snapshot boundary

The audit artifacts were copied from the ChatGPT project workspace on 2026-10-26. This directory now holds the latest selected workspace versions; the initial archived copies remain in the preceding Atlas commit. See [the preservation manifest](PRESERVATION.md) for the exact file list and boundary. `CHECKPOINT.md` is an orientation note that records the accepted progress baseline and metric drift found while reviewing the snapshot. The archived installer/catalog script, issue-rebase notes, and mega-patch script are retained as inert reference files; they are not instructions to execute.

Source repositories were not copied or changed. The audit's claims must be read against the repository heads and evidence dates recorded inside the documents. Some Markdown links use the original author's local workspace paths; those links will not resolve on other machines, though the docs also include remote links where available.

## Evidence discipline

Keep source-confirmed behavior, owner intent, historical proposal, reported behavior, inference, and runtime-verified results distinct. Keep current-file coverage and history/intent cross-reference as separate measures. A path citation proves only that a file was reached; it does not prove that all its behavior or relevant history was reconciled.
