# Latest-source file coverage register

**Observed:** 2026-10-26. This register enumerates the 913 `.rs`, `.sh`, `.py`, and `.rhai` files in the 15 checked-out repository roots used by the source census. For each root it records the observed HEAD/date, file-level dirty state, physical line count, and an occurrence count showing how many times each exact absolute local path appears in the semantic review and current-state cross-reference. The owner-accepted comparison baseline is **568 / 913** focused implementation citations and **437 / 913** history/intent citations. A mechanical exact-path recount of the current artifacts produced 808 / 913 and 724 / 913, respectively. The counting method/corpus differs from the accepted checkpoint and remains unreconciled, so the recount is provisional and does not replace that baseline.

The register is a scope-control instrument, not a claim that all 913 reviews are complete. Exact local-path mentions show reach only; they do **not** prove that the whole file, all branches, or related intentions were reconciled. The mechanical recount covers 808 files in the focused semantic review and 724 in the current-state cross-reference, but they remain unreconciled with the accepted 568/913 and 437/913 baseline. The individual disposition columns record 19 source files on each completion track: the Registry service (3 files), Identity service (15 files), and Diagnostics service (1 file) now have individual current-state and history/intent dispositions. Dispositions are a separate measure from citation reach. The other rows remain open on one or both tracks. Historical GitHub commit links and grouped analysis do not increment file-level reach or completion unless the row's own disposition and evidence are recorded. On October 26, local HEADs and source-file states were refreshed; the only dirty executable-source row is the pre-existing modified Vapor-Installer UI file. The source roots were not edited during this audit. Counts include comments and blank lines; generated/build trees and non-code material are outside this register.

The roots include parent containers and their submodules, without counting submodule contents twice: Loo-Cast; Vapor-Client container and its seven children; Platform Server container and its five services. The stale `loo-cast-flight-overhaul` project checkout is excluded from current source because it is a separate preserved historical WIP; it is documented in the evidence atlas. These source-only counters are nested inside, and never substitute for, the two broader 1,540-file tracks. The latest whole-repository recount's 1,009 path-cited files and 36 dispositions on each track are reported separately in [the inventory](latest-repository-file-inventory.md); path reach is unreconciled with the accepted 791/1,540 baseline, and dispositions are not reach counts.

## Independent coverage tracks

The audit has two separate file-level completion targets, each measured against all 913 current source files. The accepted checkpoint remains 568/913 implementation review and 437/913 history/intent cross-reference. The scan-derived table below is the current occurrence-register snapshot, still unreconciled with those accepted figures:

- **Current implementation review:** read and classify each file’s implemented behavior, ownership and relevant boundaries. The focused semantic-review path register reaches 808/913 files (105 uncited); 19/913 have individual per-file dispositions.
- **History and intent reconciliation:** relate each current file or module to its relevant historical decisions, documentation, proposals, reported behavior and reversals, or explicitly record that none is discoverable. The current-state cross-reference reaches 724/913 files (189 uncited); 19/913 have individual history/intent reconciliations.

These tracks must each reach the 913-file denominator. Their overlap is useful for locating files touched by both, but combining them into one percentage would hide the independent work still required. Exact path citation counts are conservative evidence pointers: grouped discussion without a file path does not count as file-level reach.

## Exact-path reference census

The latest reproducible absolute-path-base recount finds 808/913 files path-cited in the focused semantic review and 724/913 in the current-state cross-reference. Their separate uncited counts are 107 and 192. Per-file current-state dispositions and history/intent reconciliations are tracked separately at 19/913 in each source subset; neither reach track substitutes for or combines with the other. Do not compare these totals to the accepted checkpoint until the path-counting rules and source corpus are reconciled.

| Repository root | Source files | Focused review path-cited | Focused review not path-cited | Current-state path-cited | Current-state not path-cited |
|---|---:|---:|---:|---:|---:|
| Loo-Cast | 526 | 517 | 9 | 478 | 48 |
| Vapor-Client container | 23 | 10 | 13 | 4 | 19 |
| Vapor | 168 | 132 | 36 | 101 | 67 |
| Vapor-GUI | 31 | 26 | 5 | 19 | 12 |
| Vapor-Studio | 47 | 25 | 22 | 25 | 22 |
| Vapor-CLI | 48 | 48 | 0 | 48 | 0 |
| Vapor-Installer | 5 | 3 | 2 | 1 | 4 |
| Vapor-Steam-Entrypoint | 5 | 4 | 1 | 4 | 1 |
| Vapor-Examples | 8 | 8 | 0 | 8 | 0 |
| Vapor-Platform-Server container | 31 | 14 | 17 | 15 | 16 |
| Diagnostics Server | 1 | 1 | 0 | 1 | 0 |
| Docs Server | 1 | 1 | 0 | 1 | 0 |
| Homepage Server | 1 | 1 | 0 | 1 | 0 |
| Identity Server | 15 | 15 | 0 | 15 | 0 |
| Registry Server | 3 | 3 | 0 | 3 | 0 |
| **Total** | **913** | **808** | **105** | **724** | **189** |

See [CSV coverage register](latest-source-file-coverage.csv), [source census and known gaps](vapor-ecosystem-evidence-atlas.md#source-coverage-and-gaps), and [research index](loo-cast-vapor-research-index.md).

This is the executable-source subset of the broader [1,540-file repository inventory](latest-repository-file-inventory.md), which also tracks Markdown, manifests, service units, templates and other non-code files. The focused-review and history/intent columns below are exact-path reach indicators only; the whole-file dispositions remain separate.



The per-file path counts are regenerated from exact absolute-path mentions in the corresponding focused review and current-state cross-reference. A mention records that the file has been reached; it does not certify complete semantic review or full history/intent reconciliation.
