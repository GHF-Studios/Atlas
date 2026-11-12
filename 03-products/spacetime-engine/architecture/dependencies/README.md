# Dependencies

> **Status:** Draft — current crate dependencies should be verified against Cargo manifests.

Record the external libraries and internal domains the Engine depends on, why each is required, and which targets or features use it. The current crate uses Bevy ECS and Avian3D among other dependencies; consult `Cargo.toml` for exact versions and feature edges.

Separate build-time dependencies from runtime policy and product composition.
