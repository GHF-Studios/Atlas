# Scripting and Reflection

> **Status:** Draft — current scope and trust boundary need code-level verification.

Describe the Engine's Rhai scripting and reflection facilities, which capabilities scripts can access, and how scripts interact with engine state. Do not assume every subsystem is exposed or that arbitrary scripts are safe.

The crate currently depends on Rhai with synchronization enabled; cite concrete registrations and runtime checks before describing the surface.
