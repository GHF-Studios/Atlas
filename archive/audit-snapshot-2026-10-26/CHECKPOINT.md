# Audit checkpoint — 2026-10-26

## Metric correction

Earlier working notes included exploratory totals derived from uneven CSV row-status labels. Those rollups are not owner-approved metrics and are retired from summaries; they should not be used to estimate completion or time remaining. Current-state implementation review and history/intent reconciliation remain separate obligations. The live inventory records one whole-inventory path-reach scan, 1,359/1,540, against the unreconciled accepted comparison point of 791/1,540. This measures navigation only, not review completion.

## Accepted progress baseline

The earlier readout whose scale the owner accepted was:

| Independent measure | Accepted checkpoint |
|---|---:|
| Focused implementation review, source files path-cited | 568 / 913 |
| History/intent cross-reference, source files path-cited | 437 / 913 |
| Broader repository inventory, files path-cited | 791 / 1,540 |

These are three separate reach measures. The two source measures must not be combined: one tracks implementation review, the other history and intent. The broader inventory has its own denominator and purpose. These figures are preserved as the accepted comparison point; this snapshot did not independently reconstruct their exact counting procedure.

## What drifted

Later edits to the working artifacts replaced the accepted figures with unreconciled citation-reach recounts using a changed exact-path scan. The scan and corpus were not reconciled against the accepted baseline. Do not silently substitute a later count for the accepted comparison point or present any path count as a semantic-completion percentage. CSV row-status rollups have been retired as an invalid progress measure.

Per-file ledgers remain working notes. Their labels are not a completion measure; do not total them or use them to estimate remaining time. Path citations alone do not satisfy semantic review.

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

The next operator-path review found that `smoke-diagnostics.sh` leaves its synthetic report in persistent server state: the current API has no deletion/expiry route, and aggregate quota rejects new uploads rather than cleaning old ones. The manual public HTTP helper omits Registry even though local health checks cover all five services; the GitHub public check covers Registry only when enabled. An evidence-atlas sentence that incorrectly said local health omitted Registry was corrected. No external service was contacted.

A subsequent absolute-path-base recount found that the cited-example paragraphs and the coverage CSV had drifted apart. The recount repaired direct path references for the Vapor-Examples source files on both tracks. These remain navigation aids, not semantic completion, and do not replace the accepted 568/437 comparison baseline. The counting methods remain unreconciled with the accepted 791 whole-inventory baseline.

The next source-only operator slice found that both systemd timers set `Persistent=true` without `OnCalendar`, making the flag ineffective while their monotonic schedules remain active. `install-caddy.sh` replaces `/etc/caddy/Caddyfile` before formatting and validation; `deploy.sh` restarts Caddy later. This is a conditional rollback hazard, not a live-server finding. The timer claim is checked against the [systemd.timer manual](https://freedesktop.org/software/systemd/man/latest/systemd.timer.html). No build, test, service query, or VPS operation was performed.

A targeted refinement of the existing recovery finding checked Registry's route and database lifecycle. Current HTTP routes are GET-only, but startup runs schema/seed writes and SQLite is in WAL mode. Export's live recursive copy is therefore a conditional startup-time consistency risk, not a demonstrated steady-state write race. Restore moves the open state directory and never restarts Registry, so endpoint health alone cannot show that the restored database was adopted. SQLite's [WAL contract](https://www.sqlite.org/wal.html#the_wal_file) and [online backup guidance](https://www.sqlite.org/backup.html) support that distinction. No local archive, restore, live service, or VPS was exercised.


## October 26 — Vapor-CLI source citation reconciliation

The CLI source pass added direct path reach within Vapor-CLI. These figures were raw path reach only and remain unreconciled against the accepted 568/437/791 comparison point; they are not semantic completion. Do not use row-status labels as a second progress metric.


## October 26 — diagnostics and USF ownership contracts

The next source slice refined the Loo-Cast diagnostics/USF sections with direct module citations and recorded a best-effort telemetry boundary: bounded emitter failures are returned to callers but diagnostics publication ignores them. It also clarified typed snapshot cadences, inline-only ECS memory estimates, and the distinction between manifestation ownership and constituency. The Loo-Cast source worktree already had a modified `Cargo.lock`; it was preserved and not edited.


## October 26 — Loo-Cast combat source pass

The projectile/health slice records the scale-aware spawn path, direct transform motion, same-scale endpoint containment scan, split-peer filter, semantic hit-to-Health conversion, and the gaps between `DamageableBounds`, collision geometry, and impact effects. The endpoint-only algorithm exposes a source-confirmed tunneling condition for sufficiently large displacement; no gameplay failure was reproduced.

## October 26 — Health presentation source pass

The follow-up traced player and world health bars back through Health, USF ownership and split-peer resolution, then compared the current projection/cache with its September extraction and October cleanup history. The HUD explicitly assumes a first local Player; world bars reconcile every eligible semantic Health manifestation each frame, without producer-side distance/frustum selection, and defer cache cleanup while no player camera exists. The paired-visual recovery added in `d806e3d` is retained as a sound local invariant. No runtime or tests were run.


## October 26 — Engine UI foundation source pass

The current UI root centralizes shared text and panel tokens but no reusable layout/control kit. Adoption is partial (including a locally styled flight HUD), z-order combines named 0/100/110 layers with literal 1,840–20,000 values, and both font roles still use Bevy defaults; a bundled engine font was not found. The `Stage 6` comment has no matching Markdown definition in the checkout. No UI/runtime test was performed.


## October 26 follow-up — Loo-Cast developer-adapter slice

The adapter review records the generic Engine contracts and Loo-Cast-specific camera, collider/portal, and USF identity projection. It identifies a source-location ownership mismatch and an unresolved chart-unit-versus-metre policy at the focus ray; neither was runtime-tested. The then-current citation reach was provisional and unreconciled against the accepted baselines. Do not interpret path reach or row-status labels as semantic completion.


The same pass reviewed the embedded Developer Editor shell: live camera projection, transient docking/selection state, and a flat visualization registry shared by two separate presentation surfaces. It adds path reach, not per-file certification. No game UI was launched.

## October 26 — content graph and durable selection follow-up

Corrected the resolver history attribution after checking the actual commit diffs: generic graph resolution, graph/kind validation, and Packagepack projection predate the October extraction; `f9e8b13` moved the provider-neutral model and added candidate-supplied resolution/partial reports; `c3b0a78` was error-size and formatting cleanup, not a semantic validation expansion. The crosswalk now also traces the “Default” duplication to persistent state: an opaque `active_composition_id` selects a separate `Composition` record, seeded as `id = "default"` with no Packagepack root, while the selected Packagepack is another optional field. This is a concrete data-model mismatch with the owner’s later Packagepack-as-selection direction, distinct from any UI rendering choice. Removed retired CSV row-status rollups from the checkpoint and evidence-atlas summaries; they remain bookkeeping labels, not completion measures. No source files or worktrees were changed; no builds, tests, formatting or deployments were run.

The content crosswalk now includes the direct-edge/required-target helper matrix across all ten kinds and links the 10/21 `CreateFromContent` action to Studio's remaining two-request create-then-assign flow. This separates an owner-set product direction (Packagepack is the selection; remove the duplicate default) from the still-unworked storage migration and workspace-binding contract. The history expansion also distinguishes the first Packagepack-only resolver (`c65f1e7`), same-day generic-graph refactor (`cce0630`), and October addition of optional/provider-selected partial resolution (`f9e8b13`). These are source-and-diff findings; test definitions were not executed.

The latest content trace found a confirmed preview/execution policy seam: preview uses the provider-neutral install planner, but execution runs a second recursive `install_selector`. Preview validates the flattened graph, while execution validates each manifest's local role cardinality and selected edges. A Packagepack naming Engine A, Game G, and G's required Engine B can be rejected by preview for two effective Engines while satisfying the executor's local role checks. Per-item trees, locks and receipts are also written before the final content-index save; recovery after a later failure remains unverified. This discrepancy is source-proven but not runtime-reproduced. No build, test, formatting or deployment ran; source trees remain unchanged.

The Crate lifecycle crosswalk was integrated into the main current-state account and index. The additional finding is specific: scaffolding creates `rlib`/`staticlib`, but the manifest writer does not declare the static library for packaging; staging copies the authored root while excluding only `.git`, `target`, and `output`, and stages only declared outputs. Thus a default generated Crate package does not demonstrate a downloadable static payload, and source files may remain in the copied root. This also narrows the book's claim that staged content is not a Cargo checkout; the contradiction applies where the authored root contains Cargo files. `cargo.rs` and `cargo_reconciliation.rs` were already inspected as complete files, with relevant lineage checked; no source files changed and no build, package, test, or Workshop operation ran.

The timeline's Cargo-realization appendix now connects that October Crate packaging gap to the earlier September composition proof and links both current-state artifacts. This is a focused extension of the recent chronology; the full historical register remains commit coverage rather than semantic review of every change.

The packaging source review also recorded three additional risks in that current-state and timeline account: slug collisions can make distinct accepted IDs share an output directory; the shared copier follows symlinks without target containment; and non-dry package replacement deletes the previous output before staging/fingerprinting/receipt succeeds. Their failure or disclosure effects are inferred, not reproduced. History dates the copier/slug helper to Oct 18, package replacement to Oct 19, and the later temporary-staging test to Oct 20; that test covers preview cleanup only. No build, tests, package operation, symlink probe or Workshop upload was run.


## October 26 follow-up — voxel diagnostics and palette

The voxel inspection cross-check found that one toggle draws both spatial-demand and materialization bounds, the 16-hue palette disagrees with its seven-band comment, and a prior per-scale pipeline census was removed. Aggregate worker counters and one first-surface log remain, but they do not locate a particular stalled stage. No runtime diagnostics were collected.


## October 26 follow-up — flight and navigation policy model

The flight review found explicit capability/control/contact/assistance/safety/telemetry boundaries and a separate approach-refinement contract. It also found one multi-domain `TravelProfile`, a spacecraft constructor identical to the character profile, and a stale future-tense safety-supervisor comment despite the current evaluator. No movement/runtime behavior was tested.

## October 26 follow-up — console record and inspector boundaries

The console/inspector slice found a real shared console record contract, introduced across the engine and Vapor on October 22, without end-to-end shared ownership of source/target meaning, retention/query, presentation or tracing delivery. The engine retains 512 rows and draws each retained entry; terminal tracing remains Bevy-owned. Inspector fields distinguish direct, validated, transactional and command access, but typed metadata/widget traversal and dynamic InspectionFrame edit requests are still parallel systems with different consumers. These are source findings only; no UI/runtime or performance behavior was exercised.

## October 26 follow-up — scale construction and procedural asset contracts

The remaining Loo-Cast focused-source gaps were reviewed. The USF constructor preserves f64 while carrying/refining the hierarchy, then stores a bounded f32 leaf offset; root overflow is an intentional finite-universe wrap, and the constructor is reused by translation and authored world/voxel coordinates. Procedural assets separate replaceable presentation from semantic terrain but still expose a hardcoded narrow built-in catalog; an October 5 commit removed deterministic, periodicity, seed-sensitivity and pixel-size tests. Debug-grid behavior moved from a finite texture to shader evaluation. The two checked-in Rhai scripts are an identity freecam transform and hostless scratch, not evidence of two live features. Source and history only; no tests, scripts, build or runtime were executed.

The next cross-reference slice reconciled controller/manifestation transfer, flight requests and safety state, cruise dropout, and approach refinement against the October 6 control/navigation extraction and October 9 flight-safety integration. It confirmed that an emergency Lattice Cruise dropout clears cruise state and returns the subject to manual assistance; that state is not itself a general braking impulse or proof of collision. Approach refinement requests future detail without choosing the controlled interaction chart. This is source/history analysis only and does not establish that the reported Moon braking failure is fixed.

The next history slice traced the named procedural-world bootstrap to the September 25 `e14e928` conversion into an authored Earth–Moon proving fixture; `117ca49` separated Keplerian mechanics from spacecraft telemetry; `0e48843` expanded the canonical propagation/fixture integration; and `25af9d1` repaired player visibility reconciliation. The active fixture's exact Earth/Moon constants, spherical field, and single reference craft are Rust-owned test/game scaffolding, not yet Vapor-authored content or a reusable world pipeline. The inventory module is a nine-slot item selector, not a quantity/ownership system. No code changed outside this audit repo; no tests/builds/runtime executed.

Developer-tool history now ties the current console renderer to the October 22 shared-record migration, the inspector UI to its September 19 extraction, scalar-field drawing to the September visualization pipeline, and USF manifestation lines to the September 27 registration. Findings preserve the distinction between shared record semantics and local presentation, typed and dynamic inspector models, and semantic ECS ownership versus developer visualization. No UI/runtime behavior was exercised.

Thermal cross-reference follows aggregate energy, localized conduction and material injury to separate owners. `ThermalInjury` is consumed through Health, while direct thermal impulses resolve to the semantic body. The current inspector adapter is the dynamic request path and remains a second consumer model beside typed Transform inspection. Historical review found the old thermal architecture note removed and domain/simulation/spatial tests deleted in October cleanup commits. This records source and history only; it does not assert a gameplay or numerical failure.

Spatial/voxel cross-reference now explicitly distinguishes Avian backend colliders, portal/stencil collision topology, canonical swept collision queries, rendered voxel manifestations, and direct semantic medium sampling. Scale affinity and presentation-view demand are separate policies; voxel edits retain global order alongside a chunk index, and edit/material/contact agreement remains a cross-owner question. No high-speed collision claim was tested.

The Loo-Cast source/history pass connects deterministic construction provenance and sparse atlas discovery to the still-Rust-authored Earth/Moon fixture; it distinguishes procedural presentation prototypes from semantic assets and records Playground state/tools as tiny examples rather than a creator pipeline. Path reach alone does not certify individual file review. Accepted comparison baselines remain unchanged and unreconciled.


## October 26 follow-up — app-root role setup and tool readiness

Reviewed the app-root player/developer setup wrappers and shared implementation. Player setup owns contained directories, SteamCMD, anchor and receipt; Developer composes Player then adds Rust/Cargo and cross-target toolchain components. The combined status recommendation can send a player toward developer setup when only cross-target tools are missing. Developer teardown removes its receipt and tool paths; Player teardown removes the app-local state tree, while the separate pre-uninstall hook removes the external app-root anchor. History links this mechanism to the July 27 app-root tools introduction, July 28 control-surface consolidation, and October 21 first-launch/Rust-Analyzer changes. No setup command ran.

## October 26 follow-up — platform deployment automation and state backup

The platform-server source review connected its five-minute deploy timer to a full hard-reset/build/restart of all five services on every activation, with CI and VPS deployment selecting host Rust rather than the declared 1.97.0 toolchain. State export is better guarded: the systemd deploy route and exporter share a file lock, active stateful services are stopped during copy, configuration secrets are excluded, and retention is bounded. Direct privileged invocation of deploy.sh bypasses the lock because serialization lives in the unit. This is source/history analysis only; no VPS action, build or test ran. Citation reach figures recorded at the time were provisional and unreconciled with the accepted baseline; they are navigation evidence only.

## October 26 follow-up — Superworkspace/source-clone ownership

Compared the installed app-root source-clone tools with the newer Vapor Core Superworkspace model. Core defaults to `~/Vapor`, discovers real top-level workspaces and container submodules, and treats the manifest as a marker; app-root scripts maintain a four-repository hard-coded preset list, use host `git`, and rewrite that same manifest filename with schema-2 source-role records that Core does not parse. The resource resolver lacks Core's default root and relies on flags, environment or cwd. The Linux Steam wrapper sets cwd to the app root, so direct resource invocations need a root bridge. Clone creation and manifest registration are non-transactional. These are confirmed dual-ownership seams, not a demonstrated universal runtime failure. No clone or workspace operation ran.

## October 26 follow-up — Vapor Studio authoring, Workshop and async result routing

Reviewed the remaining Studio source/UI paths and their October 16–23 history. Studio separates the player composition from its editable Packagepack source, but the Compositions page still combines install/launch, source editing and launch configuration. Workshop browse has type filtering, paging and multi-select in code; type filtering is a required canonical UGC tag, so tag publication is part of correctness and was not verified against a live Workshop account. Service work is conflict-checked by resource and independent operations may overlap; Studio adds a bounded in-memory FIFO only after a conflict response. Both authoring and workspace-file result handlers match IDs against only the first active operation, so a later concurrent result can be dropped and remain finalizing. This is source-confirmed correlation logic with an inferred out-of-order failure mode, not a runtime reproduction. Studio also has a canonical Rust module result adapter, while the IDE dispatches the module-creation action. No build, UI, tests, service process or Workshop query was run.

Updated exact-path reaches at that checkpoint were provisional navigation figures and remained unreconciled against the accepted baseline. They are not completion measures.


## October 26 — Shared content semantics and Studio findings; citation recount updated

Reviewed the canonical `vapor_content` vocabulary, authored manifest projection, stable/exact/unresolved identity types, partial resolver, provider-neutral install plan, and Client state/policy boundary. The resolver deliberately skips optional edges and greedily selects highest satisfying dependency versions without global backtracking; the separate graph validator enforces pack cardinality and direct mod targets. Added a caveat that direct authored-manifest parser callers must enforce role exclusivity through the role-specific reader. Also completed a Studio source slice, including the service-concurrency/result-correlation mismatch and the Workshop tag dependency. Source review only; no build, test, runtime, GUI or Workshop account was used.

Updated exact-path reach at that checkpoint remained provisional and unreconciled against the accepted baseline. No row-status rollup is used as a completion measure.


## October 26 — Platform operator-script safety and lifecycle review

Reviewed the remaining VPS operator scripts and their focused tests. Identity secrets are redacted in output but can still be supplied as process arguments; the deploy trigger user has narrowly limited sudo but an unrestricted ordinary SSH shell; and the Docs smoke script uploads a placeholder over the live current release without rollback. The normal SSH docs uploader keeps the token server-side and best-effort cleans a staged public archive. State-bundle validation rejects path traversal, links, special files, duplicate members and secret-inclusive manifests, with tests covering only a subset of rejection cases and no explicit resource-limit checks. Source/history only; no scripts, tests, credentials, deploy or live service were run.

Updated exact-path reach at that checkpoint remained provisional and unreconciled against the accepted baseline. No row-status rollup is used as a completion measure.


## October 26 — SDK command metadata and Steam/root publication review

Reviewed the SDK command-spec vocabulary, app-root environment report, first-party root package/publish path and SteamCMD status/process contract. Command specs are presentation metadata for stub handlers, not an enforcement engine. Root publishing stages only `bin/` plus activation scripts and supports a review fingerprint, but the fingerprint omits file permissions, symlink targets are not constrained to the package roots, and VDF strings do not reject control newlines/tabs. SteamCMD credential ownership is delegated correctly, while its reported state root is not passed into process invocation; read-only Steam status also depends on managed-toolchain readiness, and app-build output is buffered until exit. Source/history only; no root package, SteamCMD, build or deploy ran.

Updated exact-path reach at that checkpoint remained provisional and unreconciled against the accepted baseline. No row-status rollup is used as a completion measure.


## October 26 — GUI, Installer, Steam entrypoint, and IDE host boundaries

Reviewed product routing, App-root discovery, argument forwarding, entrypoint redaction, and the two IDE process contracts. Confirmed that Steam App-root discovery is executable-relative (no Steam-folder workspace manifest required); Installer accepts but drops several `--app-root` and workflow arguments; and the Core `vapor-ide-host` is a narrow content-inspection helper distinct from service-hosted LSP traffic. Product modes share one Vapor-GUI host and Chooser adds a mode-routing hop through the Steam entrypoint. Source/history only; no executable, GUI, LSP, build or tests were run.

Exact-path reach at that checkpoint was provisional and unreconciled against the accepted baseline. No row-status rollup is used as a completion measure.


## October 26 — Full exact-path coverage of current executable-source inventory

The remaining focused-source path gaps were inspected and documented across app-root scripts, Client application/domain/provider/service, Core, GUI/IDE, Installer, SDK and server tooling. Both focused implementation and source-history/current-state cross-reference now name every source inventory path. This closes direct-reference reach only: it does not certify every line or fully resolve every historical intent. The accepted baselines (568 and 437) remain unreconciled with the mechanical method.

The wider whole-repository path scan remains provisional and unreconciled with its accepted 791 baseline. No build, test, formatter, deployment, product runtime, or server operation was used.

## October 26 — Planning-corpus and content-semantics cross-check

Reviewed the planning intake protocol, the July bootstrap snapshots, selected glossary and Rhai/USF term families, the deferred Roadmap 07 pages, and current `vapor_content` definitions. The imported glossary pages remain unprocessed evidence; their provenance names `origin/develop` without a source commit/hash, and many cite a Phase 3 execution-spec path absent from this checkout. The legacy Rhai notes preserve detailed reflection/dispatch/scoped-access designs but label themselves provisional and point into an unavailable legacy/quarantine tree. Roadmap 07 explicitly defers the Vapor capability/Rhai runtime.

Compared those layers with the owner's later content/pack definition: packs are typed manifests over content, content carries the reusable compiled payload, and a Packagepack alone may additionally carry the finished executable; “composition” is an informal Packagepack synonym. Current `ContentKind`, common payload fields, nested pack references and Packagepack cardinality rules do not express that contract. This is a recorded owner-direction/current-schema conflict, not an implemented redesign. The broader citation recount methodology changed and is not reconciled to the accepted comparison baseline. Reference-only worktrees remain unchanged; no builds, tests, formatter, deployment or runtime were used.


## October 26 — Roadmap/glossary branch state and provenance

Cross-checked the active roadmap against the decision queues and repository-local approval protocol. The roadmap hierarchy is settled and glossary migration is its first active child, but the glossary branch remains unclosed: 18 of 64 questions have answers (Q006 is qualified); Q019–Q064 are blank. The queue requires an owner-approved page-level packet before any copy. The registered source is Loo-Cast `origin/develop` without a commit/hash, and the current local Loo-Cast `main` checkout at `c070bf3` has a pre-existing dirty `Cargo.lock` and no visible `loo_cast_alpha/docs/glossary` tree or matching branch. This is a migration provenance gap, not proof the source material never existed. No source files were changed and no migration packet was created.

The all-Markdown path recount increased at that checkpoint, but remains provisional path reach and unreconciled against the accepted comparison baseline. It is not a semantic completion measure. No builds, tests, formatting, deployments, or product operations were run.

## October 26 — Premium Docs corpus crosswalk

Read and compared the Premium Docs corpus: the ownership README, architecture and development models, experience models, glossaries, repository-migration documents, rewrite bootstrap, and progress roadmap. Added a local document-by-document crosswalk distinguishing durable principles from superseded or unverified contracts. Key divergences: the older separate Vapor App Composition object versus the owner's later Packagepack identity; the four-role model versus later three-level experience language and compositional Cargo use by Composer; Launcher↔SDK mode versus separate Launcher/Studio/IDE products over one service; and proposed immutable Registry publication versus the accepted Registry catalog / Identity authorization / Steam transport model. The exact migration checklist retains sound safety discipline but is stale as a live status ledger. The old `Process/` navigation path is described but not created. Their history/intent reconciliation remains open. Source documents were not changed. Do not use the exploratory CSV row-label totals that were recorded at this checkpoint as workstream status.

The recount rescanned the local Markdown artifacts and resolves each repository-relative path against its checked-out root, accepting literal and URL-safe punctuation forms; it is navigation evidence only. The methods remain unreconciled with the accepted baseline. No build, tests, formatter, deployment, or product runtime was used.

## October 26 — Audit state restored after cross-document recount

The accepted comparison points remain **568/913 focused implementation citations**, **437/913 source history/intent citations**, and **791/1,540 broader file citations**. They are three separate historical baselines and remain unreconciled with later mechanical path scans. Current path reach is recorded in the live inventory documents; it measures exact-path navigation, not semantic completion. CSV row-status labels are not progress counters.

The broader recount found many path mentions added by indexing legacy and technical-glossary material. Those source pages remain unreviewed evidence; adding a navigational citation did not review them. No accepted baseline was reset or replaced. Source worktrees remain untouched; this audit update is local and uncommitted while the documentation repository is being prepared.

## October 26 — Workflow-design crosswalk added; counts remain independent

Reviewed three additional product-design files against their Git history, later owner decisions, and the latest source findings. The October 17 Studio-local child-service model is superseded by the shared Client service; the October 18 lifecycle design preserves separate authoring/play context but its second Composition identity, mandatory schema migration, and old Auto-Install semantics are stale; and the October 22 Launcher-coherence design is only partly implemented, with later owner direction changing Auto-Install ownership and authorizing public Workshop testing. The crosswalk does not convert its adjacent code paths into file-level reviews.

The workflow-design crosswalk was added before the repository-boundary and lifecycle crosswalks. These records do not establish that adjacent source files are semantically complete.

## October 26 — Content scaffolding and package staging hazards

Reviewed the complete source-workspace initializer and the shared Packagepack staging implementation. The basic starter creates Engine/Game source plus Packagepack metadata, but its generated Engine only prints a title and its Game library does not install gameplay; its README's local deploy command demonstrates graph/deployment mechanics, not a playable build. The source-to-link path for Crates remains unconnected, and the package stage has reachable slug-collision, symlink-copy, and non-atomic replacement hazards under the documented conditions. These are source-derived findings, not reproduced failures. No builds, tests, packaging, or publication ran.

## October 26 — Repository and product-boundary crosswalk

Reviewed the October 14 repository-boundary design and implementation plan, the October 15 full-stack lifecycle design and plan, and the October 20 product-surface decision. Parent commit `41c62e6` records the local submodule/repository-boundary transition; `7825e12` documents the later Launcher/Studio/IDE product split. Current source has separate GUI product crates and entrypoint modes, but the shared-service-only facade contract remains incomplete. The October 14 “two frontends” and bundled Studio/Installer model were superseded; the product split is an evolution of the lifecycle, not its replacement. The crosswalk also records that remote GitHub administrative state was not independently verified, and that plan checkboxes are not current runtime evidence.

The crosswalks cited three previously uncited files. The current all-Markdown path reach remains **1,359/1,540** (**181 uncited**) across 17 audit Markdown files; later crosswalks added evidence to files already cited. This remains provisional exact-path navigation reach, unreconciled with the accepted **791/1,540** baseline; it is not semantic completion. The separate accepted source baselines remain **568/913 implementation** and **437/913 history/intent**, while current mechanical source-path reach remains **913/913** in each register. No row-label aggregate is used as a progress counter. Source worktrees remain untouched; audit edits are local and uncommitted. No builds, tests, formatting, deployment, or runtime operations were performed.

The repository/product-boundary crosswalk now reconciles the October 14 migration plan with the October 20 Launcher/Studio/IDE decision and local parent/submodule history. The content-graph crosswalk compares the October 24 untracked draft against current graph/Cargo code; it identifies Packagepack's source-versus-manifest representation as unresolved and distinguishes the draft from an approved implementation contract. The workflow crosswalk also covers the October 22 owner-approved Player/Composer/Developer design: service action tiers, local Library/source separation and asynchronous discovery are partly present, but conflict requests are rejected rather than queued and product surfaces still do not enforce the tier boundaries. Later owner decisions supersede the plan's separate Composition identity and old Auto-Install/persistence assumptions. The console/editor crosswalk finds shared semantic records and Rhai lexical rules implemented, but command-catalog reuse, process-stream completeness and live visual parity remain open. A deeper Premium Docs comparison now separates surviving graph/closure/Cargo-boundary ideas from the superseded player-facing Composition object and the still-missing target-identity, constituency, and per-kind payload semantics. These are document/source dispositions, not new completion metrics. The crosswalked source worktrees remain untouched; audit edits are local and uncommitted.

## Hand-back readout — 2026-10-26

These are four distinct ledger views, not a single completion score:

| Measure | Current ledger state | What it actually means |
|---|---:|---|
| Source-path reach in semantic diff | 913/913 rows have an exact path mention (905 distinct path strings) | Every source inventory row is navigable from the diff ledger; this is not proof each file's behavior was fully assessed. |
| Source-path reach in current-state cross-reference | 913/913 rows have an exact path mention (905 distinct path strings) | Same limitation; an exact citation is not full review. |
| Source current-state review certification | 6/913 marked reviewed; 907/913 remain “not certified as fully reviewed” | This strict ledger status has only been advanced for the focused content-graph slice. |
| Source history/intent reconciliation | 6/913 lineage reconciled; 806/913 only path-cited; 101/913 not individually cross-referenced | Historical citation coverage is not commit-by-commit semantic reconciliation. |
| Whole-inventory current-state dispositions | 78/1,540 marked reviewed; 1,462/1,540 not assessed | The ledger's explicit current-state status, across source and non-source files. |
| Whole-inventory history/intent dispositions | 56/1,540 marked reconciled; 1,484/1,540 not reconciled | A separate history measure; it must not be combined with current-state dispositions. |
| Whole-inventory exact-path reach | 1,359/1,540 cited; 181/1,540 uncited | Navigation reach only; unreconciled with the accepted 791/1,540 comparison method. |

The prior accepted checkpoints (568/913 focused implementation citations; 437/913 history/intent citations; 791/1,540 broader file citations) remain historical comparison points, not replacements for the present ledger states. This readout resolves the apparent contradiction between “all paths are cited” and “the review is far from done”: the first is true for source-path reach; the second is true for explicit review and history dispositions. No aggregate across these rows is meaningful. The audit is still a large working corpus, not a finished five-year account. The owner asked to pause soon for a substantive review, so the next step is to walk through this state and choose which remaining audit track has the most value before extending it further.
