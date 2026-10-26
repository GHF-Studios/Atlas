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

Later edits to the working artifacts replaced those figures with 747 / 913, 648 / 913, and 944 / 1,540. A mechanical recount of the current artifacts now yields 755 / 913, 653 / 913, and 959 / 1,540; both sets remain unreconciled against the accepted baseline. The later edits also added separate per-file disposition counts (19 / 913 on each source track and 36 / 1,540 on each broader track). Those later numbers were generated through a changed exact-path scan and a new disposition ledger. They are not demonstrated to be directly comparable to the accepted baseline, and the dispositions are a distinct measure from citation reach. Treat the later values as unreconciled until the method and corpus are compared. Do not silently substitute them for the accepted baseline or present either kind of count as a semantic-completion percentage.

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

The original objective remains latest-state-first, evidence-based understanding of Loo-Cast and Vapor and how they formed. It is not a character-by-character audit of early prototype code. Historical depth should grow toward the present, with older work expanded where it explains a surviving idea, reset, reversal, or ownership boundary. The ChatGPT project source mirror is read-only, and no pre-Git 2021 archive has been established in this snapshot. After this checkpoint was created, the owner directed that the audit resume locally while they create its destination documentation repository. The resumed pass added path-by-path history for Diagnostics, current-state plus history coverage for Docs Server, and a six-file current-state/history map for Homepage Server. The latest passes mapped Platform Server deployment/recovery, docs publication and operator ingress against the clean live `a98770a` checkout and relevant July–October commits: five-service deployment versus three-service recovery, lock bypass, plaintext-capable HTTP token transport, renderer-dependent bundle output, a live-mutating docs smoke, and a September change that removed direct pre-DNS routes while leaving old HTTP-by-IP instructions. A Registry source review found that startup seeding can leave retired provider repository records in a persisted database after renames, while the fresh-database test misses that upgrade path; live DB state remains unknown. A deeper execution-path pass traced the broken bootstrap to the September Registry commit and confirmed that CI only syntax-checks it; all server build/test/deploy paths also bypass their declared Rust pin. This remained source/history review only; no VPS, archive, restore, build, test, request, or publish was run.

## Preservation state

All pre-existing files under `artifacts/` were copied into this snapshot without editing their contents. Source worktrees remain untouched. The local audit repository is now the working copy for continued review until the owner supplies the destination repository.

## Continuation after checkpoint

The next operator-path review found that `smoke-diagnostics.sh` leaves its synthetic report in persistent server state: the current API has no deletion/expiry route, and aggregate quota rejects new uploads rather than cleaning old ones. The manual public HTTP helper omits Registry even though local health checks cover all five services; the GitHub public check covers Registry only when enabled. An evidence-atlas sentence that incorrectly said local health omitted Registry was corrected. Coverage documents at that checkpoint showed the mechanical scan (755/653/959) separately from the unreconciled prior scan (747/648/944) and retain the owner's accepted 568/437/791 comparison baseline; per-file dispositions remain a separate measure. No external service was contacted.

A subsequent absolute-path-base recount found that the cited-example paragraphs and the coverage CSV had drifted apart. The current focused and cross-reference counts are 761/913 and 658/913 (152 and 255 uncited), with all eight Vapor-Examples source files now path-cited on both tracks. These remain mechanical reach counts, not semantic completion, and do not replace the accepted 568/437 comparison baseline. The corresponding inventory reach is now 962/1,540 (up from 959 in the preceding artifact snapshot); both are unreconciled with the accepted 791 baseline.

The next source-only operator slice found that both systemd timers set `Persistent=true` without `OnCalendar`, making the flag ineffective while their monotonic schedules remain active. `install-caddy.sh` replaces `/etc/caddy/Caddyfile` before formatting and validation; `deploy.sh` restarts Caddy later. This is a conditional rollback hazard, not a live-server finding. The timer claim is checked against the [systemd.timer manual](https://freedesktop.org/software/systemd/man/latest/systemd.timer.html). No build, test, service query, or VPS operation was performed.

A targeted refinement of the existing recovery finding checked Registry's route and database lifecycle. Current HTTP routes are GET-only, but startup runs schema/seed writes and SQLite is in WAL mode. Export's live recursive copy is therefore a conditional startup-time consistency risk, not a demonstrated steady-state write race. Restore moves the open state directory and never restarts Registry, so endpoint health alone cannot show that the restored database was adopted. SQLite's [WAL contract](https://www.sqlite.org/wal.html#the_wal_file) and [online backup guidance](https://www.sqlite.org/backup.html) support that distinction. No local archive, restore, live service, or VPS was exercised.


## October 26 — Vapor-CLI source citation reconciliation

The CLI source pass added direct path reach for the remaining 31 implementation-review and 38 cross-reference gaps within Vapor-CLI; its 48 executable-source units now have path citations in both documents. The fresh mechanical counts are 792/913 focused source citations and 696/913 cross-reference citations, with 121 and 217 files still uncited on those separate tracks. The broader all-file inventory recount is 993/1,540. All figures are raw path reach, remain unreconciled against the accepted 568/437/791 baseline, and are not semantic completion. Per-file dispositions remain 19/913 for each source track and 36/1,540 for each all-file track.


## October 26 — diagnostics and USF ownership contracts

The next source slice refined the Loo-Cast diagnostics/USF sections with direct module citations and recorded a best-effort telemetry boundary: bounded emitter failures are returned to callers but diagnostics publication ignores them. It also clarified typed snapshot cadences, inline-only ECS memory estimates, and the distinction between manifestation ownership and constituency. The latest mechanical path counts now read 796/913 focused, 704/913 cross-reference, and 997/1,540 broader inventory. Accepted baselines (568/437/791) remain unreconciled; the citation counts are reach only. The Loo-Cast source worktree already had a modified `Cargo.lock`; it was preserved and not edited.


## October 26 — Loo-Cast combat source pass

The projectile/health slice records the scale-aware spawn path, direct transform motion, same-scale endpoint containment scan, split-peer filter, semantic hit-to-Health conversion, and the gaps between `DamageableBounds`, collision geometry, and impact effects. The endpoint-only algorithm exposes a source-confirmed tunneling condition for sufficiently large displacement; no gameplay failure was reproduced. At that checkpoint, focused review and cross-reference reached 798/913 and 711/913 source paths, and the all-file citation reach was 999/1,540. The accepted 568/437/791 baselines remain unreconciled and separate.

## October 26 — Health presentation source pass

The follow-up traced player and world health bars back through Health, USF ownership and split-peer resolution, then compared the current projection/cache with its September extraction and October cleanup history. The HUD explicitly assumes a first local Player; world bars reconcile every eligible semantic Health manifestation each frame, without producer-side distance/frustum selection, and defer cache cleanup while no player camera exists. The paired-visual recovery added in `d806e3d` is retained as a sound local invariant. Latest path reach is 800/913 focused, 714/913 cross-reference, and 1,001/1,540 all-file; accepted baselines remain separate and unreconciled. No runtime or tests were run.


## October 26 — Engine UI foundation source pass

The current UI root centralizes shared text and panel tokens but no reusable layout/control kit. Adoption is partial (including a locally styled flight HUD), z-order combines named 0/100/110 layers with literal 1,840–20,000 values, and both font roles still use Bevy defaults; a bundled engine font was not found. The `Stage 6` comment has no matching Markdown definition in the checkout. Latest path reach is 802/913 focused, 716/913 cross-reference, and 1,003/1,540 all-file. These are provisional reach counts only; accepted baselines remain separate. No UI/runtime test was performed.


## October 26 follow-up — Loo-Cast developer-adapter slice

The adapter review records the generic Engine contracts and Loo-Cast-specific camera, collider/portal, and USF identity projection. It identifies a source-location ownership mismatch and an unresolved chart-unit-versus-metre policy at the focus ray; neither was runtime-tested. Citation reach was refreshed independently: focused source 806/913 (107 uncited), source history/intent 721/913 (192 uncited), whole-repository 1,007/1,540 (533 uncited). The accepted baselines remain 568/913, 437/913, and 791/1,540; all latest values remain provisional and unreconciled. Per-file disposition counts remain 19 on each source track and 36 on each whole-repository track. These reach measures and disposition measures remain separate.


The same pass reviewed the embedded Developer Editor shell: live camera projection, transient docking/selection state, and a flat visualization registry shared by two separate presentation surfaces. It adds path reach, not per-file certification. No game UI was launched.


## October 26 follow-up — voxel diagnostics and palette

The voxel inspection cross-check found that one toggle draws both spatial-demand and materialization bounds, the 16-hue palette disagrees with its seven-band comment, and a prior per-scale pipeline census was removed. Aggregate worker counters and one first-surface log remain, but they do not locate a particular stalled stage. Citation reach now stands at focused source 808/913 (105 uncited), source history/intent 724/913 (189 uncited), and whole repository 1,009/1,540 (531 uncited). The earlier accepted baselines remain 568/913, 437/913, and 791/1,540; current reach is unreconciled. Disposition counts remain separate and unchanged. No runtime diagnostics were collected.


## October 26 follow-up — flight and navigation policy model

The flight review found explicit capability/control/contact/assistance/safety/telemetry boundaries and a separate approach-refinement contract. It also found one multi-domain `TravelProfile`, a spacecraft constructor identical to the character profile, and a stale future-tense safety-supervisor comment despite the current evaluator. Current citation reach: focused source 808/913 (105 uncited), source history/intent 725/913 (188 uncited), whole repository 1,009/1,540 (531 uncited). The accepted comparison points remain unchanged and unreconciled. No movement/runtime behavior was tested.

## October 26 follow-up — console record and inspector boundaries

The console/inspector slice found a real shared console record contract, introduced across the engine and Vapor on October 22, without end-to-end shared ownership of source/target meaning, retention/query, presentation or tracing delivery. The engine retains 512 rows and draws each retained entry; terminal tracing remains Bevy-owned. Inspector fields distinguish direct, validated, transactional and command access, but typed metadata/widget traversal and dynamic InspectionFrame edit requests are still parallel systems with different consumers. These are source findings only; no UI/runtime or performance behavior was exercised. Exact-path reach remains focused 808/913, source history/intent 725/913, and whole-repository 1,009/1,540; accepted 568/437/791 baselines remain unchanged and unreconciled. Disposition counts remain separate.

## October 26 follow-up — scale construction and procedural asset contracts

The remaining Loo-Cast focused-source gaps were reviewed. The USF constructor preserves f64 while carrying/refining the hierarchy, then stores a bounded f32 leaf offset; root overflow is an intentional finite-universe wrap, and the constructor is reused by translation and authored world/voxel coordinates. Procedural assets separate replaceable presentation from semantic terrain but still expose a hardcoded narrow built-in catalog; an October 5 commit removed deterministic, periodicity, seed-sensitivity and pixel-size tests. Debug-grid behavior moved from a finite texture to shader evaluation. The two checked-in Rhai scripts are an identity freecam transform and hostless scratch, not evidence of two live features. Source and history only; no tests, scripts, build or runtime were executed. Current exact-path reach: focused source 817/913 (96 uncited), source history/intent 731/913 (182 uncited), full repository 1,015/1,540 (525 uncited). Accepted baselines remain 568/437/791, separate and unreconciled; per-file dispositions remain separate.
