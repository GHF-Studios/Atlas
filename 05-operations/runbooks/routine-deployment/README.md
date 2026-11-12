# Routine Deployment

- CI exact-revision request → root approval → request-specific worker → health/smoke checks
- Stale requests may be superseded; do not bulk-dispatch failed approvals
- Check latest status/runbook before action