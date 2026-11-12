# Dependencies

- `loo-cast-game` → `spacetime-engine` Rust crate
- Packagepack executable → Engine + Game via Cargo
- Vapor manifest dependencies express typed content composition separately from Cargo dependency edges
- Cargo autotests/doctests disabled for Engine and Game crates; no test-coverage claim