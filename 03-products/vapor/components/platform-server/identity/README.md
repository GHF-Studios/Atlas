# Identity

> **Status:** Draft — service boundary grounded in accepted identity contracts.

Identity owns account linkage, roles, authentication/session state, and access decisions. The accepted model anchors Vapor profiles to Steam and allows GitHub attachment for development/root authorization; Steam browser identity, Steamworks verification, Vapor roles, and publishing authority remain distinct.

Other services should use Identity-issued authorization rather than inventing incompatible auth policy. Verify current routes and implementation before describing a production flow.
