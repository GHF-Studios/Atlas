# Architecture

- Three registered projects: Spacetime Engine · Loo-Cast Game · Loo-Cast Packagepack
- Packagepack manifest selects Engine and Game by Vapor IDs; executable links both Rust crates
- Game crate installs Engine gameplay/developer plugins; current behavior is not isolated in a complete Game library
- Steam product boundary: Packagepack executable/manifest; Vapor runtime remains separately installed