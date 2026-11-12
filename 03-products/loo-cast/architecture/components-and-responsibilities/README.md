# Components and Responsibilities

- Engine: reusable runtime plus current Loo-Cast gameplay systems/adapters
- Game: thin install function adding Engine game/developer plugins
- Packagepack: executable entrypoint calling `spacetime_engine::run(loo_cast_game::install)`
- Steam locator: separate Vapor-Client repo component; locates Vapor Home and routes launch