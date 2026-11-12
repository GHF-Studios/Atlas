# Current State

> **Status:** Draft — source docs checked 2026-11-12; latest Platform deployment snapshot is dated 2026-11-09.

Vapor has a substantial Rust client and separate terminal, graphical, installer, Studio, and Steam-entrypoint applications. The standalone installation and state migration is still in progress. Platform Server documentation records an independent-service deployment slice; Registry currently stores source topology rather than typed content, and Build Cache supports signed snapshot validation/promotion without worker-backed production or a durable native-build operation lifecycle.

The latest deployment status document records `0/2` target snapshots and no configured worker. This is a dated source snapshot, not a live health check; verify the deployment-status record before updating it. Studio already documents local project discovery, manifest editing, composition preview, and review flows, but these do not establish the missing server-owned catalog or complete acquisition path.
