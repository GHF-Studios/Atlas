# Lifecycle

- Player acquisition/install/verify/repair/update are distinct operations
- Subscription adds availability; it does not silently edit a playable composition
- Shared service reports operation results; frontend must not claim success early
- Install lifecycle design/current code: [service contract](https://github.com/GHF-Studios/Vapor/blob/a633583/docs/vapor-client-service.md)