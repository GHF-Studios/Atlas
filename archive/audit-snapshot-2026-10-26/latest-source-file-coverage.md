# Latest-source file coverage register

**Observed:** 2026-10-26. This register enumerates the 913 `.rs`, `.sh`, `.py`, and `.rhai` files in the 15 checked-out repository roots used by the source census. For each root it records the observed HEAD/date, file-level dirty state, physical line count, and an occurrence count showing how many times each exact absolute local path appears in the semantic review and current-state cross-reference. The owner-accepted comparison baseline is **568 / 913** focused implementation citations and **437 / 913** history/intent citations. The latest exact-path recount produces **913 / 913** on both independent tracks. The counting method/corpus differs from the accepted checkpoint and remains unreconciled, so these are provisional reach counts and do not replace that baseline.

The register is a scope-control instrument, not a claim that all 913 reviews are complete. Exact local-path mentions show reach only; they do **not** prove that the whole file, all branches, or related intentions were reconciled. The latest recount covers all 913 files in the focused semantic review and all 913 in the current-state cross-reference, still unreconciled with the accepted 568/913 and 437/913 baselines. The CSV's row-level status labels are uneven and must not be added up or presented as a completion measure. The other rows remain open on one or both review obligations. Historical GitHub commit links and grouped analysis do not establish file-level completion unless the row's own disposition and evidence are recorded. On October 26, local HEADs and source-file states were refreshed; the only dirty executable-source row is the pre-existing modified Vapor-Installer UI file. The source roots were not edited during this audit. Counts include comments and blank lines; generated/build trees and non-code material are outside this register.

The roots include parent containers and their submodules, without counting submodule contents twice: Loo-Cast; Vapor-Client container and its seven children; Platform Server and its five services. The stale `loo-cast-flight-overhaul` project checkout is excluded from current source because it is a separate preserved historical WIP; it is documented in the evidence atlas. These source-only counters are nested inside, and never substitute for, the two broader 1,540-file tracks. The latest all-Markdown whole-repository path reach is 1,359/1,540, reported separately in [the inventory](latest-repository-file-inventory.md). Per-file status labels in that ledger are supporting bookkeeping, not another completion metric; neither they nor path citations certify semantic review.

## Independent coverage tracks

The audit has two separate file-level completion targets, each measured against all 913 current source files. The accepted checkpoint remains 568/913 implementation review and 437/913 history/intent cross-reference. The scan-derived table below is the current occurrence-register snapshot, still unreconciled with those accepted figures:

- **Current implementation review:** read and classify each file’s implemented behavior, ownership and relevant boundaries. Exact-path reach is 913/913, but individual semantic findings have only been written for reviewed slices; a path mention is not a review.
- **History and intent reconciliation:** relate each current file or module to its relevant historical decisions, documentation, proposals, reported behavior and reversals, or explicitly record that none is discoverable. Exact-path reach is 913/913, but individual history/intent findings have only been written for reviewed slices; a path mention is not a reconciliation.

These tracks must each reach the 913-file denominator. Their overlap is useful for locating files touched by both, but combining them into one percentage would hide the independent work still required. Exact path citation counts are conservative evidence pointers: grouped discussion without a file path does not count as file-level reach.

## Exact-path reference census

The latest reproducible absolute-path-base recount finds 913/913 files path-cited in the focused semantic review and 913/913 in the current-state cross-reference. Exact-path reach means each row has a direct reference in that document; it does not certify line-complete review or full historical reconciliation. The two review obligations remain separate and open; no aggregate of inconsistent row labels is used as a completion figure. Do not compare these totals to the accepted checkpoint until the path-counting rules and source corpus are reconciled.

| Repository root | Source files | Focused review path-cited | Focused review not path-cited | Current-state path-cited | Current-state not path-cited |
|---|---:|---:|---:|---:|---:|
| Loo-Cast | 526 | 526 | 0 | 526 | 0 |
| Vapor-Client container | 23 | 22 | 1 | 19 | 4 |
| Vapor | 168 | 154 | 14 | 128 | 40 |
| Vapor-GUI | 31 | 26 | 5 | 19 | 12 |
| Vapor-Studio | 47 | 47 | 0 | 47 | 0 |
| Vapor-CLI | 48 | 48 | 0 | 48 | 0 |
| Vapor-Installer | 5 | 3 | 2 | 1 | 4 |
| Vapor-Steam-Entrypoint | 5 | 4 | 1 | 4 | 1 |
| Vapor-Examples | 8 | 8 | 0 | 8 | 0 |
| Vapor-Platform-Server container | 31 | 30 | 1 | 25 | 6 |
| Diagnostics Server | 1 | 1 | 0 | 1 | 0 |
| Docs Server | 1 | 1 | 0 | 1 | 0 |
| Homepage Server | 1 | 1 | 0 | 1 | 0 |
| Identity Server | 15 | 15 | 0 | 15 | 0 |
| Registry Server | 3 | 3 | 0 | 3 | 0 |
| **Total** | **913** | **913** | **0** | **913** | **0** |

See [CSV coverage register](latest-source-file-coverage.csv), [source census and known gaps](vapor-ecosystem-evidence-atlas.md#source-coverage-and-gaps), and [research index](loo-cast-vapor-research-index.md).

This is the executable-source subset of the broader [1,540-file repository inventory](latest-repository-file-inventory.md), which also tracks Markdown, manifests, service units, templates and other non-code files. The focused-review and history/intent columns below are exact-path reach indicators only; the whole-file dispositions remain separate.



The per-file path counts are regenerated from exact absolute-path mentions in the corresponding focused review and current-state cross-reference. A mention records that the file has been reached; it does not certify complete semantic review or full history/intent reconciliation.
