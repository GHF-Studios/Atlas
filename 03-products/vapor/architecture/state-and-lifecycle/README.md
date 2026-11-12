# State and Lifecycle

- Vapor Home owns installed runtime/tools, caches, local state, and mutable app data
- Steam Packagepack depot owns only product manifest/executable/allowlisted sidecars
- Client service owns compositions/install policy/persistence; provider operations act on files/Steam
- Standalone move out of Steam directory remains in progress