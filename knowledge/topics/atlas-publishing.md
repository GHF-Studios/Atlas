+++
id = "atlas-publishing"
kind = "topic"
title = "Atlas build and publication lifecycle"
summary = "Atlas CI validates and packages the source; Vapor Platform Server builds and publishes the selected revision to the VPS."
claim_status = "source-verified"
parent = "atlas-system"
sources = [".github/workflows/validate-and-package.yml", "README.md", "atlas.toml"]
+++

## Source checks and build artifact

Atlas CI validates records, checks JavaScript syntax, runs the test suite, builds the static site under `_site` with base path `/atlas/`, and uploads that build as a workflow artifact. That artifact is useful for inspection; it is not the production deployment transport.

## VPS publication

GitHub is the recoverable source and CI host. The GHF Studios Platform Server deploy process fetches `VAPOR_ATLAS_REF` (default `main`) from Atlas, validates and builds it with its source revision embedded in `atlas.json`, then atomically switches the VPS `current` release symlink. Caddy serves that static release at `https://vapor.ghf-studios.site/atlas/`, independently of the `/docs/` service. The Platform Server's deploy timer checks every five minutes; its GitHub Actions workflow can also trigger deployment. The deploy implementation lives in [Vapor-Platform-Server](https://github.com/GHF-Studios/Vapor-Platform-Server), especially `deploy/scripts/deploy-atlas.sh` and `deploy/scripts/deploy.sh`.

The publication path is active and was verified by a successful Platform Server deploy and public HTTP smoke checks on 2026-10-26. The current generated site is a disposable visualization, not an approved Atlas design; see the owner-directed decision record. Deployment success establishes that the site was served, not that its content or design has owner approval.

## Deliberate operational limits

Atlas itself does not manage DNS or server routing, deploy a backend, synchronize GitHub issues, pull records from other repositories, or provide a collaborative web editor. Those are not current capabilities. Atlas is a static site; the separately owned Platform Server handles hosting and deployment. Source links in a build are pinned to the source revision when the build environment provides it.
