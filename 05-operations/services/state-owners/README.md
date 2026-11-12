# State Owners

> **Status:** Draft — service contracts own schema and persistence decisions.

For each stateful service, identify what it stores, who may write it, how it is exported/imported, and which recovery process applies. Distinguish service state from derived static output and client-local state.

Use this map to compose backups without transferring data authority to the Platform dashboard.
