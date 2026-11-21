# System Boundaries

- **Loo-Cast source:** three sibling registered content projects; no Steam app manifest in Vapor Client root
- **Steam payload:** Packagepack manifest + per-target executable + explicitly allowlisted libraries
- **Vapor Home:** runtime, tools, local state; not stored in game Steam directory
- **Platform:** process/deployment coordination; service handlers/state remain service-owned
- **Source:** [Loo-Cast](https://github.com/GHF-Studios/Loo-Cast/blob/598e98c/README.md) · [Platform](https://github.com/GHF-Studios/Vapor-Platform-Server/blob/65ade3c/README.md)