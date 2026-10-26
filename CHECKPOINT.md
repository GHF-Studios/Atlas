# Audit checkpoint — 2026-10-26

## Accepted progress baseline

The earlier readout whose scale the owner accepted was:

| Independent measure | Accepted checkpoint |
|---|---:|
| Focused implementation review, source files path-cited | 568 / 913 |
| History/intent cross-reference, source files path-cited | 437 / 913 |
| Broader repository inventory, files path-cited | 791 / 1,540 |

These are three separate reach measures. The two source measures must not be combined: one tracks implementation review, the other history and intent. The broader inventory has its own denominator and purpose. These figures are preserved as the accepted comparison point; this snapshot did not independently reconstruct their exact counting procedure.

## What drifted

Later edits to the working artifacts replaced those figures with 747 / 913, 648 / 913, and 944 / 1,540. They also added separate per-file disposition counts (19 / 913 on each source track and 36 / 1,540 on each broader track). Those later numbers were generated through a changed exact-path scan and a new disposition ledger. They are not demonstrated to be directly comparable to the accepted baseline, and the dispositions are a distinct measure from citation reach. Treat the later values as unreconciled until the method and corpus are compared. Do not silently substitute them for the accepted baseline or present either kind of count as a semantic-completion percentage.

There is also an internal inconsistency: the research index retains an 18-file disposition count in one paragraph while its current summary and the ledgers say 19. This is evidence that the counter sweep was incomplete.

## What exists in this snapshot

- A large semantic-diff ledger, written current-state first and then traced through selected historical changes.
- A current-state cross-reference, an evidence atlas, and a navigational research index.
- A chronological timeline, a rendered timeline diagram, and an origin/intent reconstruction.
- Whole-repository and source-only inventory ledgers.
- A draft cross-product architecture plan and the previously approved workflow-boundaries design.
- Several unrelated or supporting working artifacts retained unchanged for provenance; see the README.

The documents contain substantial useful analysis, including current Loo-Cast/Vapor findings and several Platform Server service reviews. They are not yet a single internally consistent, owner-reviewed account. Their volume and exact-path counts are not proof of completion.

## Still missing before the audit can be called done

1. Reconcile the accepted baseline with the later path-scan method without overwriting the original comparison point.
2. Resolve stale counters and duplicated status prose across the index and ledgers.
3. Continue the two source tracks independently: implementation coverage and history/intent cross-reference.
4. Extend those tracks across non-source files using the broader repository inventory, without treating a path mention as full semantic review.
5. Reconcile the latest-state findings against the owner's decisions, reported behavior, and older design material; label evidence and uncertainty.
6. Review the current snapshot as a coherent set, identify overlapping documents and authority order, and let the owner redirect the next phase before resuming the long audit.

The original objective remains latest-state-first, evidence-based understanding of Loo-Cast and Vapor and how they formed. It is not a character-by-character audit of early prototype code. Historical depth should grow toward the present, with older work expanded where it explains a surviving idea, reset, reversal, or ownership boundary. The ChatGPT project source mirror is read-only, and no pre-Git 2021 archive has been established in this snapshot. After this checkpoint was created, the owner directed that the audit resume locally while they create its destination documentation repository. The resumed pass added path-by-path history for Diagnostics, current-state plus history coverage for Docs Server, and a six-file current-state/history map for Homepage Server. The latest passes mapped Platform Server deployment/recovery, docs publication and operator ingress against the clean live `a98770a` checkout and relevant July–October commits: five-service deployment versus three-service recovery, lock bypass, plaintext-capable HTTP token transport, renderer-dependent bundle output, a live-mutating docs smoke, and a September change that removed direct pre-DNS routes while leaving old HTTP-by-IP instructions. This remained source/history review only; no VPS, archive, restore, build, test, request, or publish was run.

## Preservation state

All pre-existing files under `artifacts/` were copied into this snapshot without editing their contents. Source worktrees remain untouched. The local audit repository is now the working copy for continued review until the owner supplies the destination repository.
