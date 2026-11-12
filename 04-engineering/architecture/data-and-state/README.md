# Data and State

- Vapor Client owns local composition/state; providers handle filesystem/cache/installed/workspace/Workshop operations
- Server services own separate state stores; Platform coordinates backup/deploy/recovery
- Atlas is static publication output with no mutable Atlas server state