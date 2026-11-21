# Current State

## Snapshot — 2026-11-21

This is a snapshot of checked-out source and its documentation, not a live-service check or a release announcement. The relevant local repositories are [Loo-Cast](https://github.com/GHF-Studios/Loo-Cast), [Vapor-Client](https://github.com/GHF-Studios/Vapor-Client), [Vapor-Platform-Server](https://github.com/GHF-Studios/Vapor-Platform-Server), and [Vapor-Registry](https://github.com/GHF-Studios/Vapor-Registry). The checkouts are at different revisions, so this snapshot should be revisited as the source repositories change.

A concrete first-party path exists in source: Loo-Cast defines the Spacetime Engine, Loo-Cast Game, and Packagepack as sibling content artifacts. Its documented Vapor workflow validates and packages that content, then previews the shared and platform Steam depots through an allowlist. The preview does not publish to Steam; publication remains a separate action.

Vapor Client is documented as the standalone runtime and tools, with its separate installation and update lifecycle still in progress. The Loo-Cast Steam product is a distinct Packagepack assembled from the Loo-Cast source tree; it is not the Vapor Client installer.

Platform Server source describes independently deployed services and their operations. The Registry service currently describes itself as a source-topology registry, while the separate Vapor-Registry repository holds reviewed metadata for identities, first-party Steam app details, and permissions. A typed content catalog and its Workshop and publishing decisions remain future work in the checked documentation.

These sources establish implemented or documented paths, not current public reachability or deployment health. This review did not verify the live services or perform the package-and-preview workflow. For the section’s product and responsibility map, see [Product Map](../03-product-map/README.md), [Product Relationships](../04-product-relationships/README.md), and [Authority and Ownership](../08-authority-and-ownership/README.md).
