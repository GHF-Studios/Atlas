# System Boundaries

> **Status:** Draft — artifact and service boundaries are established more clearly than gameplay scope.

Separate the Loo-Cast product workspace, its three content artifacts, the Vapor runtime and Registry, the Steam app/depot, and proof-of-concept code in `Vapor-Examples`. The Loo Cast Steam app provides the first-party Packagepack through depots; it is not a Workshop publication.

Do not place Vapor state, tools, source checkout, or writable runtime state in the Steam app payload; see the source workspace's allowlist as the operational contract.
