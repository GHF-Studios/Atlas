# Atlas

Atlas is GHF Studios’ versioned source for knowledge about its products,
decisions, questions, evidence, work, and history. Its public site is generated
from this repository; the site is a navigable view, not a separate source of
truth.

## Start here

- **Readers:** open the [Atlas homepage](https://ghf-studios.github.io/Atlas/).
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

The current site is a review preview of Atlas itself and the preserved audit.
Its vocabulary and sample records remain provisional. Broader knowledge
import waits for owner review of the entrypoint.

`atlas.json` is the current machine-readable read model. It contains the
versioned record list plus a normalized `graph.nodes` / `graph.edges`
projection; `records` remain authoritative, and the graph projection is
derived during each build. A `parent` field emits a `parent` edge, while each
typed `relations` entry emits its declared edge. Consumers should check
`schema_version` before relying on the export shape.
