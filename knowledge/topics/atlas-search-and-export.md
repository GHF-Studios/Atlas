+++
id = "atlas-search-and-export"
kind = "topic"
title = "Atlas search and machine-readable export"
summary = "Atlas provides small client-side search and a versioned static JSON graph export; neither is a server API."
claim_status = "source-verified"
parent = "atlas"
sources = ["site/assets/search.js", "tools/atlas.py"]
+++

## Browser search

The home page fetches the generated `atlas.json` and performs a small client-side substring search over each record’s title, kind, claim status, and body. It displays at most twelve matches. If the export cannot be loaded, search is disabled with a message and the browse pages remain available.

This is suitable for the current small bootstrap. It is not a full-text search service, does not provide faceted query syntax, and has no server component.

## JSON read model

`atlas.json` currently declares `schema_version = 1`, Atlas configuration, authored records, and `graph.nodes` / `graph.edges`. Each node includes ID, kind, and claim status. Parentage and typed relations become graph edges. The export is rebuilt from the repository on each site build.

Consumers should check the schema version. The export is public static data; no authenticated or write API currently exists.
