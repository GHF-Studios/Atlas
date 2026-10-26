# Latest repository file inventory

**Observed:** 2026-10-26. This inventory enumerates 1,540 non-ignored files in the 15 checked-out Git repositories under `~/Vapor`, including non-code material. It includes tracked files and non-ignored untracked files; it excludes ignored/generated output and does not expand submodule gitlinks twice. The two untracked October 24 content-graph documents are included. The owner-accepted comparison baseline is **791 / 1,540** files path-cited. A mechanical recount of current artifact Markdown produced the previous 959 figure; the latest recount is 999; its comparability has not been established, so it is explicitly provisional and does not replace that baseline.

| Measure | Count | Meaning |
|---|---:|---|
| Repository files | 1,540 | Current non-ignored files across 15 Git roots; not every generated or ignored file on disk |
| Rust/Rhai/shell/Python source | 913 | The narrower code census tracked separately in [source coverage](latest-source-file-coverage.md) |
| Markdown | 455 | Documentation, design, plans, operator records, READMEs and other Markdown |
| TOML | 82 | Cargo, Vapor, tool, service and other TOML manifests/configuration |
| Files with an exact absolute path mention in the latest recount (unreconciled) | 999 | Provisional citation reach only; not comparable to the accepted baseline yet |
| Files without such an exact mention in that recount | 581 | Provisional; grouped discussion does not count as per-file reach |
| All-file current-state dispositions recorded per file | 36 / 1,540 | Explicit per-file status; citation reach does not prove review |
| All-file history/intent reconciliations recorded per file | 36 / 1,540 | Separate per-file status; citation reach does not prove cross-reference |
| Dirty or untracked files | 4 | Loo-Cast `Cargo.lock`; Vapor Installer UI formatting; two untracked Vapor content-graph documents |

| Repository | Files | Markdown | TOML | Rust |
|---|---:|---:|---:|---:|
| Loo-Cast | 557 | 6 | 11 | 523 |
| Vapor-Client container | 262 | 228 | 3 | 21 |
| Shared Vapor | 383 | 162 | 23 | 167 |
| Vapor-GUI | 41 | 3 | 6 | 31 |
| Vapor-Studio | 58 | 6 | 3 | 47 |
| Vapor-CLI | 76 | 20 | 4 | 46 |
| Vapor-Installer | 12 | 1 | 4 | 5 |
| Vapor-Steam-Entrypoint | 11 | 1 | 3 | 5 |
| Vapor-Examples | 26 | 2 | 14 | 8 |
| Vapor-Platform-Server container | 64 | 17 | 1 | 0 |
| Diagnostics Server | 7 | 2 | 2 | 1 |
| Docs Server | 7 | 2 | 2 | 1 |
| Homepage Server | 7 | 2 | 2 | 1 |
| Identity Server | 21 | 2 | 2 | 15 |
| Registry Server | 8 | 1 | 2 | 3 |

The companion [CSV](latest-repository-file-inventory.csv) records repository, relative path, extension, tracked/untracked state, dirty state, byte/line count, and exact-path mentions in the current research artifacts. It is a scope ledger and reproducibility aid, not proof that a file has been semantically reviewed or reconciled with its history. Maintain two independent per-file dispositions as review proceeds: (1) current behavior/ownership and (2) relevant history/intent, including an explicit “no relevant evidence found” disposition where appropriate. Neither disposition may be inferred from a path mention, and neither may be merged into a single completion percentage. Its counts intentionally distinguish files from submodule directory entries; the code-only register remains useful for prioritizing executable source.

## What this inventory does and does not say

- The 455 Markdown files are not all equally authoritative. The next review must distinguish normative architecture, dated decisions, implementation docs, operational instructions, historical/imported notes, and placeholders.
- The 82 TOML files include both semantic manifests and ordinary build/configuration files; their mere presence does not imply equal design significance.
- An exact local path can appear because a paragraph cites one line or discusses a file at module level. It does not imply complete file review.
- A missing exact path can still be covered by a grouped module analysis, but that coverage should be located and scoped rather than inferred.
- This inventory is one snapshot. Re-run only after deliberately refreshing repository HEADs and dirty state; do not silently mix later source with the October 26 refresh.
- Pre-Git 2021 work, inaccessible conversation history, and external assets are not enumerated here. Their absence is a documented evidence gap, not evidence they never existed.
