# Installer

> **Status:** Draft — component role grounded in the Vapor-Installer README.

The precompiled `vapor-installer` is an app-root maintenance and workflow shim. Normal status, install, repair, and uninstall actions call Vapor's shared operations; the graphical Installer module is hosted by Vapor-GUI.

The installer should not require Rust or `rust-script` for shipped first-run maintenance. Exact preservation and erasure boundaries must remain explicit.
