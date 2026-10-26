+++
id = "atlas-publishing"
kind = "topic"
title = "Atlas build and publication lifecycle"
summary = "GitHub Actions validates and packages Atlas; the intended public site is on the Strato VPS at /atlas/."
claim_status = "source-verified"
parent = "atlas"
sources = [".github/workflows/validate-and-package.yml", "README.md", "atlas.toml"]
+++

## Current continuous integration

The GitHub Actions workflow validates records, checks `site/assets/search.js` syntax, runs the test suite, and builds a static site under `_site` with base path `/atlas/`. It uploads the result as a workflow artifact on pushes, pull requests, and manual runs. It does not publish the production website.

GitHub is the recoverable source and CI host. The intended public address is `https://vapor.ghf-studios.site/atlas/`, served from the GHF Studios Strato VPS. The server route, document root, and transfer mechanism are not configured by this repository yet. This is a target, not a claim that the new site is already live. The current generated site is a disposable visualization, not an approved Atlas design; see the owner-directed decision record.

## Deliberate operational limits

The current workflow does not transfer files to the VPS, manage DNS or server routing, deploy a backend, synchronize GitHub issues, pull records from other repositories, or provide a collaborative web editor. Those are not current capabilities. Atlas is intended to remain a static site in this first deployment; no application server is needed for its current pages.
