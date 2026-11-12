# Docs Server

> **Status:** Draft — service role and Atlas publication must remain separate.

Vapor Docs Server owns uploaded or generated documentation artifacts and version/current pointers. Atlas is built from its own Git source and served as a separate static tree at `/atlas/`; it does not pass through the Docs service.

Keep route, validation, and retention details in the Docs publication contract.
