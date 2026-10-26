+++
id = "atlas-site"
kind = "topic"
title = "Atlas website and information architecture"
summary = "The current static site has home, map, timeline, questions, archive, and per-record pages, with shared navigation and styling."
claim_status = "source-verified"
parent = "atlas"
sources = ["tools/atlas.py", "site/assets/style.css"]
+++

## Current pages

The generator currently publishes these routes:

- **Home** (`index.html`): product orientation, Atlas system records, open review question, and search.
- **Knowledge map** (`map.html`): records grouped by kind, plus the configured kind and claim-status definitions.
- **Timeline** (`timeline.html`): dated event records in chronological order. It does not invent dates for undated material.
- **Questions** (`questions.html`): records whose kind is `question`.
- **Preserved audit** (`archive.html`): a file index for the historical Loo-Cast/Vapor audit snapshot.
- **Record pages** (`records/<id>.html`): one generated page per authored record, including status, body, links, and sources.

Every page shares a header, navigation, footer, stylesheet, and search script. These routes are a small initial information architecture, not a final claim about all Atlas workflows. The current “map” groups by kind; it is not yet an interactive graph visualization.

## Presentation implementation

`site/assets/style.css` defines the dark responsive visual system. The pages are plain static HTML, and the browser search behavior is in `site/assets/search.js`. The generated pages use a configurable base path so the same build can be hosted at a repository subpath or a root path.
