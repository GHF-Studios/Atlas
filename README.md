# Atlas

Atlas is one of GHF Studios’ products, alongside Vapor and Loo-Cast. Its role
is to make the organization’s products, decisions, evidence, questions, work,
and history understandable. This repository is the authored source; the
published site and JSON are generated views. Atlas is the subject of its first
knowledge set, so its own product intent, data, tools, site, and limits are
documented here before importing broader product knowledge.

## Start here

- **Readers:** start with [Atlas as a product](knowledge/topics/atlas-product.md)
  and the generated system guide at the intended [VPS address](https://vapor.ghf-studios.site/atlas/).
- **Authors:** start with [`atlas.toml`](atlas.toml) and the typed Markdown
  records under [`knowledge/`](knowledge/).
- **Developers:** run the commands below; the generator uses only Python’s
  standard library.
- **Historical audit:** the [preserved Loo-Cast/Vapor bundle](archive/audit-snapshot-2026-10-26/README.md)
  remains working evidence, not owner-approved canon. Its exact contents and
  preservation boundary are in [`PRESERVATION.md`](archive/audit-snapshot-2026-10-26/PRESERVATION.md).

## Validate, build, preview

```sh
python3 tools/atlas.py validate
python3 tools/atlas.py build --output dist
python3 tools/atlas.py serve --port 8000
```

Records use TOML frontmatter followed by Markdown. Stable IDs connect records;
explicit claim status distinguishes owner direction, source-verified facts,
reports, inference, proposals, unresolved questions, and historical snapshots.
Dates are optional. Only dated `event` records appear in the generated
timeline.

The current site explains Atlas itself and preserves a separate historical
audit snapshot. Its vocabulary and sample records remain provisional. Atlas
currently has no server, accounts, online editing, discussion system, issue
synchronization, multi-repository ingestion, or automatic interpretation of
commits. Its three primary views are **Search** (find records by text and
kind), **Connections** (follow authored typed links), and **Timeline** (dated
events). Questions are a record kind, not a parallel product area. Relation
labels are shown as authored; their vocabulary and semantics remain open. How
it works, the preserved audit, and JSON export are contextual references. See
the [site information architecture](knowledge/topics/atlas-site.md)
and the [scope record](knowledge/topics/atlas-scope.md).

`atlas.json` is the current machine-readable read model. It contains the
versioned record list plus a normalized `graph.nodes` / `graph.edges`
projection; `records` remain authoritative, and the graph projection is
derived during each build. A `parent` field emits a `parent` edge, while each
typed `relations` entry emits its declared edge. The export also identifies
the source revision when one is available. Consumers should check
`schema_version` before relying on the export shape.

## Hosting

GitHub is Atlas’s versioned source and CI host; it does not host the production
website. CI validates the records, builds the static files, and stores them as
a workflow artifact. The Platform Server also checks out Atlas as a source
submodule, fetches its configured ref (default `main`), validates and builds it,
then publishes a versioned static release to the GHF Studios Strato VPS. Caddy
serves that release at `https://vapor.ghf-studios.site/atlas/`, separately from
the `/docs/` service. The published `atlas.json` identifies the source revision
used for each build.
