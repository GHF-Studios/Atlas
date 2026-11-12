# Deployment Process

- CI request → freshness/identity checks → root approval → exact-revision worker → health/smoke checks
- Request-specific worker; polling retired in latest report
- Stale/superseded commits must not be bulk-dispatched