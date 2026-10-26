+++
id = "atlas-authoring"
kind = "topic"
title = "Atlas authoring and source of truth"
summary = "Knowledge is authored as typed Markdown records in Git; the site and JSON are reproducible views of that source."
claim_status = "source-verified"
parent = "atlas"
sources = ["README.md", "atlas.toml", "knowledge/topics/atlas-authoring.md"]
+++

## Where knowledge is authored

Atlas records live as Markdown files under `knowledge/`. Each begins with TOML frontmatter between `+++` delimiters. Metadata gives the record a stable ID, kind, title, and claim status; optional fields add a date, a parent, typed relations, or repository-relative source paths. The rest of the file is the human-readable body.

`atlas.toml` declares the current record kinds and claim-status vocabulary. The records, configuration, and generator are versioned together in this Git repository. The rendered website is generated output and should be rebuilt from these sources.

## Editing workflow

1. Edit or add a record in the directory matching its kind.
2. Run `python3 tools/atlas.py validate` to check metadata, IDs, links, dates, and cited paths.
3. Build with `python3 tools/atlas.py build --output dist` or preview with `python3 tools/atlas.py serve --port 8000`.
4. Review the rendered page and the machine export before committing.

The validator currently checks repository structure and references. It does not judge whether prose is true, whether evidence is persuasive, or whether a record belongs in the model. Those remain editorial responsibilities.
