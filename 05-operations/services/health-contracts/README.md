# Health Contracts

> **Status:** Draft — document each service's actual health contract.

Record health endpoints or checks, expected response semantics, dependency behavior, and what a passing result establishes. Distinguish liveness from feature readiness and user workflow success.

Use service-owned DTOs for readiness; do not infer it from an admin panel or a generic `healthy` status.
