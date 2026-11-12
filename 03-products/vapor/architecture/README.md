# Architecture

- `Vapor` source workspace: core/content/runtime and SDK crates
- Separate product frontends: CLI · GUI · Studio · Installer · Steam entrypoint
- Shared user-local Client service owns durable state and semantic operations
- Platform Server is a separate remote service ecosystem; not the local client