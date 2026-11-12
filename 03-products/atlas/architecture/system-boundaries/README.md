# System Boundaries

- Atlas owns source content and its repository history
- Platform Server owns publication/deployment tooling and serves built files
- No mutable Atlas server state; edits flow through Git
- **Source:** [Atlas publication contract](https://github.com/GHF-Studios/Vapor-Platform-Server/blob/65ade3c/docs/atlas-publication-contract.md)