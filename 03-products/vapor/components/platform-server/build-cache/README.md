# Build Cache

> **Status:** Draft — current object is a signed target snapshot, not a compiler-result cache.

Build Cache validates and promotes signed Cargo target-directory snapshots and exposes the current snapshot per target. It does not choose or provision a builder, own a durable build-job lifecycle, or cache independent compiler invocations.

The source contract records zero of two current target snapshots and no worker-backed snapshot production as of its latest deployment evidence; verify before updating that status.
