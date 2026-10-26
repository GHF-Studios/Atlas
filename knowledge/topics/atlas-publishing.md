+++
id = "atlas-publishing"
kind = "topic"
title = "Atlas build and publication lifecycle"
summary = "GitHub Actions validates and builds Atlas, then deploys the static Pages site from main or a manual run."
claim_status = "source-verified"
parent = "atlas"
sources = [".github/workflows/pages.yml", "README.md"]
+++

## Current publication path

The GitHub Actions workflow validates records, checks `site/assets/search.js` syntax, and builds a static site under `_site` with the `/Atlas/` base path. It uploads that directory as a Pages artifact. A push to `main` or a manual workflow dispatch deploys the artifact to GitHub Pages; pull requests build but do not deploy.

The repository is therefore the recoverable source for both content and publication machinery. The deployed site is reproducible output, not the sole copy of Atlas knowledge.

## Deliberate operational limits

The current workflow deploys the GitHub Pages artifact only. It does not deploy a backend or VPS service, synchronize GitHub issues, pull records from other repositories, or provide a collaborative web editor. Those are not current capabilities.
