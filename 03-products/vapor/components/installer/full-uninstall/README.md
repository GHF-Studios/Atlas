# Full Uninstall

> **Status:** Draft — exact removal behavior is safety-critical and must follow the installer contract.

Document the explicit inventory and confirmation required for full Vapor erasure, the external helper that waits for the running installer to exit, and the state that is intentionally preserved.

The Installer README says Steam game files and user-managed Rust/Cargo installations outside Vapor Home are preserved. Do not weaken or generalize this contract without source evidence.
