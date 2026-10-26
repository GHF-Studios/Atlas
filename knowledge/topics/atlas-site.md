+++
id = "atlas-site"
kind = "topic"
title = "Atlas website and information architecture"
summary = "The static site has a home entrypoint and three primary reading views: Search, Connections, and Timeline, plus record pages and contextual references."
claim_status = "source-verified"
parent = "atlas-system"
sources = ["tools/atlas.py", "site/assets/style.css", "site/assets/connections.js"]
+++

## Current routes and their jobs

The generator publishes pages at distinct semantic levels:

- **Home** (`index.html`): the entrypoint explains Atlas and routes readers to a view. The brand link returns here; it is not a data view.
- **Search** (`search.html`): primary record lookup, with full-text query and a sub-tab for each configured record kind. Questions are filtered here, not given a parallel top-level destination.
- **Connections** (`connections.html`): primary traversal over directed edges derived from the `parent` and `relations` fields. Readers can focus a record and filter by relation type and direction. Links navigate to record pages or refocus the view on another endpoint. Relation labels are shown as authored; the vocabulary and semantics remain open.
- **Timeline** (`timeline.html`): dated event records only. It does not invent dates for undated material or import the preserved audit's historical timeline.
- **How it works** (`system.html`): author and maintainer reference for the current record-to-site pipeline, clearly separated from Atlas's product purpose and styled as a system reference rather than a peer knowledge view.
- **Record pages** (`records/<id>.html`): generated object pages with status, body, parent, incoming/outgoing relations, and sources. They are reached from Search, Connections, Timeline, or links between records; each one is not a navigation tab.
- **Preserved audit** (`archive.html`) and **JSON export** (`atlas.json`): secondary historical-source and machine-data references, linked from relevant contexts and the footer. The selected audit snapshot is copied into the generated site; Markdown files have readable Atlas pages with local links, downloadable originals, and revision-pinned GitHub source links. Other files such as CSV, SVG, PlantUML, logs, and scripts are served as preserved downloads/assets.

The brand links to the home entrypoint. Search, Connections, and Timeline are distinct primary reading views: lookup, relationship traversal, and chronology. There is no separate Questions destination because `question` is a record kind, not an independent subsystem. How it works is a separated system reference; the archive and JSON export are contextual references. Connections is an accessible relationship list with traversal links, not a spatial graph visualization. Its filters expose currently authored edge labels without asserting that the relation ontology is complete.

## Presentation implementation

`site/assets/style.css` defines the dark responsive visual system. The pages are plain static HTML, and the dedicated Search page uses `site/assets/search.js` to filter the generated JSON index. The generated pages use a configurable base path so the same build can be hosted at a repository subpath or a root path.
