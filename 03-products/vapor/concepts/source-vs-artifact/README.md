# Source vs Artifact

> **Status:** Draft — source, build output, release, and snapshot are separate records.

Distinguish source repositories and revisions from content identities, built application releases, target build snapshots, and provider-acquired bytes. A repository may contain many content items; an artifact has its own immutable identity and provenance.

Atlas is authored source; its published static site is derived output. Vapor Artifact serves signed application releases; Build Cache stores signed Cargo target snapshots.
