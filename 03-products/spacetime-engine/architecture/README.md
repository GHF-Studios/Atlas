# Architecture

- `SpacetimeEnginePlugin`: reusable engine wiring
- `EngineApp`: alias for Bevy `App`; host/window/logging is application policy
- Vapor resolves Engine/Game roles; Rust API is not a universal ABI
- ECS entities: runtime storage/manifestation, not automatically semantic identity