# Platform Server

> **Status:** Draft — current server topology grounded in Platform Server documentation checked 2026-11-12.

Vapor Platform Server coordinates deployment and operations for public web and server services. Production is documented as independent service processes behind Caddy and systemd; each service keeps its own routes, state, and business logic.

Platform owns deployment coordination, shared operator navigation, and whole-system recovery. The separate Vapor Registry repository owns Registry service authority; the `Vapor-Registry-Server` service is a deployment component, not the authority repository.
