# Interfaces

- Engine manifest ID: `ghf-studios/loo-cast/spacetime-engine`
- Game ID: `ghf-studios/loo-cast/loo-cast-game`; manifest selects Engine
- Packagepack ID: `ghf-studios/loo-cast/loo-cast-packagepack`; selects Engine + Game
- Runtime interface: `EngineApp`/install closure in current Rust source; not a stable cross-language ABI