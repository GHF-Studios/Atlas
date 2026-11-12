# Dependencies

> **Status:** Draft — dependency inventory must come from manifests and service contracts.

Record cross-repository, runtime, and service dependencies that affect Vapor's operation. Distinguish source dependencies, runtime services, optional providers, and target architecture dependencies that are not yet active.

For example, Build Cache is not a shared compiler cache, and no production native builder currently produces target snapshots; keep those distinctions explicit.
