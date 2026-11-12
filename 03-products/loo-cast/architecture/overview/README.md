# Architecture Overview

- Loo-Cast workspace manifest registers Engine · Game · Packagepack as siblings
- Engine owns reusable Bevy/ECS, spatial, physics, voxel, thermal, portal, tooling domains
- Game adapter composes current Loo-Cast gameplay into Engine host
- Packagepack links runnable product; composition is not a Steam Workshop relationship