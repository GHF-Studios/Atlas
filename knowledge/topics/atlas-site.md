+++
id = "atlas-site"
kind = "topic"
title = "Atlas website and information architecture"
summary = "The static site has a home entrypoint, Search with type sub-tabs and a Structure sub-view, a separate Timeline, record pages, and secondary references."
claim_status = "source-verified"
parent = "atlas-system"
sources = ["tools/atlas.py", "site/assets/style.css"]
+++

## Current routes and their jobs

The generator publishes pages at distinct semantic levels:

- **Home** (`index.html`): the entrypoint explains Atlas and routes readers to a view. The brand link returns here; it is not a data view.
- **Search** (`search.html`): primary record lookup, with full-text query and a sub-tab for each configured record kind. Questions are filtered here, not given a parallel top-level destination.
- **Structure** (`structure.html`): subordinate Search view for following parent groupings. Cross-links are inspected on each record page. Structure is linked from Search, not promoted as a top-level tab or a second record catalogue.
- **Timeline** (`timeline.html`): dated event records only. It does not invent dates for undated material or import the preserved audit's historical timeline.
- **How it works** (`system.html`): author and maintainer reference for the current record-to-site pipeline, clearly separated from Atlas's product purpose and styled as a system reference rather than a peer knowledge view.
- **Record pages** (`records/<id>.html`): generated object pages with status, body, parent, incoming/outgoing relations, and sources. They are reached from Search, Structure, Timeline, or links between records; each one is not a navigation tab.
- **Preserved audit** (`archive.html`) and **JSON export** (`atlas.json`): secondary historical-source and machine-data references, linked from relevant contexts and the footer.

The brand links to the home entrypoint. Search and Timeline are the primary knowledge tabs; Structure is nested under Search; How it works is a separated system reference. There is no separate Questions destination because `question` is a record kind, not an independent subsystem. Record-type and claim-label definitions live in the system reference, not in the Structure view. The archive and JSON export are intentionally secondary. Structure is a readable hierarchy, not an interactive graph visualization.

## Presentation implementation

`site/assets/style.css` defines the dark responsive visual system. The pages are plain static HTML, and the dedicated Search page uses `site/assets/search.js` to filter the generated JSON index. The generated pages use a configurable base path so the same build can be hosted at a repository subpath or a root path.
