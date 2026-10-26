# Historical Glossary Corpus Map

**Purpose:** locate the inherited ideas without upgrading them to doctrine. This is a provenance and concept-family map, not an exhaustive candidate review, migration approval, or per-page line-complete assessment.

## Provenance and authority

The current parent-repository inventory contains 125 Vapor glossary pages and 27 technical glossary notes imported from a Loo-Cast `origin/develop` snapshot. The source register gives no import commit, branch object ID, or immutable archive identifier. It explicitly says the corpus has no authority and is unprocessed; an atomized source would still be unvetted. The current Loo-Cast checkout does not contain the named source tree, so source-level fidelity to the original branch cannot be re-established from this checkout alone. See the [corpus register](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/corpus-register.md:1>) and [planning protocol](</home/leslieghf/Vapor/Vapor-Client/docs/planning/README.md:1>).

The imported term pages are not a flat set of finalized definitions. Their metadata counts are 116 `WIP-draft`, 6 `draft`, 1 `legacy-bridge`, 1 `merged-legacy`, and 1 `future-pressure`. Thirty-three explicitly contain “owner-answer-informed” framing, which records historical answers at the time of authoring; those sentences are not automatically equal to the later decisions in this conversation. Twenty glossary pages still point to a Phase 3 execution-spec path absent from the checked-out source tree. The tech glossary's own index labels the workflow-runtime pages as legacy evidence and marks Rhai reflection/bridge/value-semantics notes as provisional or quarantine evidence.

Navigation is itself incomplete: the corpus register lists all source pages, but the glossary directory has no local index README; the tech glossary does have an index. The exhaustive intake register is an inventory mechanism, not a human concept map. The separate October 26 roadmap/glossary decision queue remains open and requires an owner-approved page-level migration packet before copying or rewriting anything. See [decision-gate cross-reference](current-state-semantic-cross-reference.md#october-26--roadmap-hierarchy-glossary-branch-and-the-unclosed-approval-gate).

## Concept families and their later fate

### Vapor capabilities, Rhai, hooks, and Rust surfaces

The broadest family (about 25 Capability-prefixed glossary terms plus callbacks, contexts, scopes, host contracts, and Rust surface terms) proposes one heterogeneous capability graph with separate authored declaration, Rust host contract, runtime instance, projection, callback, and signature concepts. Its best surviving insight is the separation of **data/description**, **host authority**, **scoped access**, **invoked behavior**, and **runtime scheduling**. Projected, nested, handle-oriented contexts and different callback signatures are especially close to the later user discussion of handles as retained values that grant access only during a valid semantic and temporal window, and hooks whose schedule/phase and implementation cardinality may be part of their type.

The pages are explicit drafts, however, and they make concrete choices not yet settled by that later conversation: detailed Type/Trait/Extension-Slot/Signature taxonomies; `decl_ctx` and callback-context rules; dynamically narrowed and re-opened path masks; a fixed-point bootstrap; generic dispatch; and a capability “kernel” / native registration architecture. Some details may be useful machinery; none should be adopted merely because there is a page for it. Later owner direction adds a broader recursive authoring/metaprogramming loop: Rhai can define capability structure and generate bounded Rust/WASM, which can then shape later Rhai surfaces, with a hard immutable core and separate dynamic runtime layer. The current Vapor Roadmap 07 still defers the capability/Rhai runtime, and the current source does not implement that full generative lifecycle.

The later authority boundary is sharper than the old term family: Layer 1 is hard-coded in the engine; Layer 2 is statically composed into the immutable core and is not unloadable after launch; Layer 3 can load/unload sandboxed Rust as WASM. That direction supersedes the glossary's proposed platform-native `.dll`/`.so`/`.dylib` implementation artifacts as the general unloadable-mod mechanism. Toolchain pinning remains essential for statically linked content. The owner also treated USF as an Engine subsystem, not a Vapor-wide Capability/product pillar; a capability runtime may support USF, but the two are not synonyms.

**Disposition:** preserve the separation questions and handle/scope concepts as high-value design evidence; treat each concrete graph/type/lifecycle prescription as unvetted until reconciled with the later Layer 1/2/3 model, hook schedule/phase, retained-data/reacquired-access lifetime, and Rust/WASM sandbox boundary. Current source comparison is in the [script/compiler and content review](loo-cast-vapor-semantic-diff-review.md#october-25--the-ide-understands-parts-of-rust-structure-source-authoring-still-has-two-competing-doors) and [deferred runtime roadmap review](loo-cast-vapor-semantic-diff-review.md#october-26--sdk-command-metadata-and-steamroot-publication-review); these references are adjacent evidence, not proof that the complete scripting model is implemented.

### USF and spatial/temporal simulation model

The USF family treats USF as a public/API-facing Spacetime Engine subsystem. It separates declared meaning/support (`Scale`, `Scale Definition`, `Scale Support`) from realization (`Scale Realizer`), observer projection (`Scale View`), and active instance graph. It proposes 71 logarithmic spatial levels, `1000^3` local chunk units, scale-bound Metrics, Phenomena as significant world-state carriers, and a model in which the active scale is the primary change-authority scale while other scales can remain simulated with scaled time. The separate USF glossary preserves the same authority-vs-representation distinction at higher resolution.

Those boundaries are valuable and align with the later warning against one universal numeric `Scale`; the numeric laws and topology are not settled by their presence in the WIP pages. A particularly important chronology gap is that these imported definitions say temporal scale is context-dependent and does not derive from spatial scale, while the owner later proposed a strict space/time coupling (10× space corresponds to 10× time), with local gameplay-specific timescale adjustments carrying the exceptions. Spatial work is the current priority and temporal implementation was explicitly future scope, but the conceptual conflict remains open and must be recorded rather than silently resolved in favor of the older glossary.

**Disposition:** USF's Engine ownership and authority/representation questions are strong surviving design signals; the 71-level, chunk-size, Metric/Phenomenon lifecycle, capability-driven runtime, and temporal independence claims are historical model details requiring reconciliation. Current Engine code has scale/chart/residency and collision mechanisms, but earlier code review found their behavior and ownership incomplete; neither this corpus nor type names prove USF parity. See the [USF glossary cross-check](vapor-ecosystem-evidence-atlas.md#the-archived-usf-glossary-against-the-current-implementation) and [current spatial/temporal review](current-state-semantic-cross-reference.md#spatial-scale-and-collision-authority-scaffolding-exists-coverage-is-not-proven).

### Content, packs, mod types, and artifacts

The imported content family is an important ancestor of today's fixed ten-kind vocabulary and carries useful distinctions among source files, build outputs, distributable artifacts, local cache forms, identities, fingerprints, and compatibility. But its contract is older: Engine/Game are represented by required built-in `core_mod`/`base_mod` crate roles; Enginepack and Gamepack select one fixture plus extensions; Packagepack composes those two packs; Mods are delivered as native dynamic libraries; and Packs may have local aggregated payload forms.

The owner has since explicitly fixed the ten kinds as Packagepack, Enginepack, Gamepack, Modpack, Engine, Game, EngineMod, GameMod, ExtensionMod, and Crate (renamed from Library). In the later model, Packs are typed manifests; they do not physically contain their content. Content carries the reusable statically linkable artifact. Only a Packagepack may also carry the completed executable. Composer combines existing Content and Packs into new Packs and may use Cargo compositionally, without authoring constituent Rust source. All three non-Package packs may describe mutually exclusive alternatives; optional dependencies, mandatory dependency typing, cardinality, conflicts and extension-mod targets still need a single coherent graph contract. “Composition” is an informal synonym for the playable Packagepack, not a second first-class product object.

The old artifact distinctions are worth retaining only where they map cleanly to the new identity/download story: authoring source, per-content compiled static library, pack manifest, and final Packagepack executable are different payload roles. Workshop's inability to conveniently split item payloads and the possible use of GitHub releases are delivery questions, not reasons to put content “inside” a pack semantically. The current type model and distribution pipeline were previously reviewed as mismatching this owner direction; see [the owner-model comparison](vapor-ecosystem-evidence-atlas.md#owner-model-to-compare-against) and [the package/build boundary analysis](loo-cast-vapor-semantic-diff-review.md#october-26--packagepack-cargo-generation-handles-enginegame-only-and-is-not-wired-into-client).

### Vapor product, source, and user journey

The old notes already contain the durable product impulse: Steam as acquisition/bootstrap, source outside the install, managed tools, genuine Git/Cargo/Workshop underneath, a pleasant player-to-creator path, and support for independently authored projects plus coordinated multi-repository development. They also describe Vapor as a Steam-specific SDK/launcher/distribution layer above engines and games. This anticipates the full-stack content lifecycle the owner still wants.

The repo/product layout and UI assumptions are dated. The imported root README has Vapor-Root with four submodules (Vapor, SDK, Launcher, Examples), and labels GUI as future guides/tutorials. Product terms such as Vapor Launcher, SDK, “Player Mode / Modpack Author Mode / Developer Mode,” and direct Source/Artifact behavior predate the current shared local Client service, separate Launcher/Studio/IDE direction, Composer/Developer boundary, Steam Entrypoint modes, and owned full GUI lifecycle. Keep these as intent history, not a current topology.

### Workflow runtime vs product operations

The tech glossary describes a Rust/Bevy workflow runtime with typed workflow/stage families, per-instance state, bounded stage buffers, sender caches, timeout policy and invariant ledgers. This is an internal scheduled runtime mechanism in the Engine/USF lineage. It must not be conflated with Vapor Client's user-facing operations, queues, progress records, or conflict scheduler merely because both use “workflow.” The latter has a service protocol and shared operation records but has its own ownership and correlation issues; the names alone do not prove shared machinery.

### Explicitly superseded and future-pressure terms

The source set itself contains useful self-corrections: `Capability Slot Type` is marked legacy-bridge and split into newer draft terms; `Scripting Projection Meta-Layer` is merged into Capability Projection API; “Zone-Era Concepts” says zones should not remain primary world authority and points toward Phenomena; and `steam-like-platform-contracts` is marked future pressure. These are states inside an unvetted historical corpus, not repository-wide authoritative promotions. They show that even this import had revisions and supersession before it reached the newer glossary monoliths.

## What this pass did and did not establish

- Established the 125 + 27 source inventory, local page sizes, frontmatter status distribution, explicit owner-answer-informed subset, missing source snapshot identity, missing glossary index, and major cross-family contradictions.
- Read representative and high-impact pages from each family and compared them against the later owner decisions, current roadmap state, and already-reviewed current source findings.
- Did **not** atomize or pairwise-review all 152 sources; did not certify every line in each page; did not recover the exact original `origin/develop` commit; did not migrate or approve any term; and did not mark the pages as current-state-reviewed or history-reconciled in the inventory.
- The appendix below is exact-path discovery aid only. Its links improve navigation; they do not process or reconcile the referenced source entries.

## Source-page path index


### Vapor glossary source files

- [Artifact Compatibility Envelope.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Artifact%20Compatibility%20Envelope.md>)
- [Artifact.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Artifact.md>)
- [Asymmetric Failure Doctrine.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Asymmetric%20Failure%20Doctrine.md>)
- [Build Artifact.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Build%20Artifact.md>)
- [Callback Context Type.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Callback%20Context%20Type.md>)
- [Callback Scope Envelope.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Callback%20Scope%20Envelope.md>)
- [Callback Signature.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Callback%20Signature.md>)
- [Callback Type.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Callback%20Type.md>)
- [Capability Bootstrap Fixed-Point Cycle.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Capability%20Bootstrap%20Fixed-Point%20Cycle.md>)
- [Capability Callback.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Capability%20Callback.md>)
- [Capability Contract.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Capability%20Contract.md>)
- [Capability Declaration.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Capability%20Declaration.md>)
- [Capability Extension Slot.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Capability%20Extension%20Slot.md>)
- [Capability Framework.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Capability%20Framework.md>)
- [Capability Graph Diagnostics.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Capability%20Graph%20Diagnostics.md>)
- [Capability Graph Scope Envelope.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Capability%20Graph%20Scope%20Envelope.md>)
- [Capability Instance Signature.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Capability%20Instance%20Signature.md>)
- [Capability Instance.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Capability%20Instance.md>)
- [Capability Kernel.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Capability%20Kernel.md>)
- [Capability Module.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Capability%20Module.md>)
- [Capability Node.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Capability%20Node.md>)
- [Capability Path.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Capability%20Path.md>)
- [Capability Projection API.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Capability%20Projection%20API.md>)
- [Capability Resolution Semantics.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Capability%20Resolution%20Semantics.md>)
- [Capability Role.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Capability%20Role.md>)
- [Capability Runtime.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Capability%20Runtime.md>)
- [Capability Slot Type.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Capability%20Slot%20Type.md>)
- [Capability Trait Signature.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Capability%20Trait%20Signature.md>)
- [Capability Trait.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Capability%20Trait.md>)
- [Capability Type Signature.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Capability%20Type%20Signature.md>)
- [Capability Type.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Capability%20Type.md>)
- [Capability-Centric Semantics.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Capability-Centric%20Semantics.md>)
- [Capability.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Capability.md>)
- [Chunk.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Chunk.md>)
- [Closed Runtime and Open Design.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Closed%20Runtime%20and%20Open%20Design.md>)
- [Complexity Gradient.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Complexity%20Gradient.md>)
- [Contract Family.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Contract%20Family.md>)
- [Contract.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Contract.md>)
- [Declaration Scope Envelope.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Declaration%20Scope%20Envelope.md>)
- [Distributable Artifact.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Distributable%20Artifact.md>)
- [Dynamic Authority Resolution.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Dynamic%20Authority%20Resolution.md>)
- [Engine Mod.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Engine%20Mod.md>)
- [Engine.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Engine.md>)
- [Enginepack.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Enginepack.md>)
- [Entity Plane Split.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Entity%20Plane%20Split.md>)
- [Entity Proxy.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Entity%20Proxy.md>)
- [Execution-Reconciliation Dual Core.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Execution-Reconciliation%20Dual%20Core.md>)
- [Extension Mod.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Extension%20Mod.md>)
- [Fingerprint.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Fingerprint.md>)
- [Game Mod.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Game%20Mod.md>)
- [Game.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Game.md>)
- [Gamepack.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Gamepack.md>)
- [Global Capability API Graph.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Global%20Capability%20API%20Graph.md>)
- [Global Capability Surface.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Global%20Capability%20Surface.md>)
- [Kernel Artifact.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Kernel%20Artifact.md>)
- [Loo Cast.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Loo%20Cast.md>)
- [Managed Ambiguity.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Managed%20Ambiguity.md>)
- [Metric.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Metric.md>)
- [Mod Artifact Structure.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Mod%20Artifact%20Structure.md>)
- [Mod Authoring Structure.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Mod%20Authoring%20Structure.md>)
- [Mod Contract Source.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Mod%20Contract%20Source.md>)
- [Mod Implementation Source.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Mod%20Implementation%20Source.md>)
- [Mod Runtime Representation.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Mod%20Runtime%20Representation.md>)
- [Mod Structure.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Mod%20Structure.md>)
- [Modding Contract.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Modding%20Contract.md>)
- [Modding Runtime.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Modding%20Runtime.md>)
- [Modpack.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Modpack.md>)
- [Observer-Relative Simulation.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Observer-Relative%20Simulation.md>)
- [Packagepack.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Packagepack.md>)
- [Phase 3 Vapor Testing Suite.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Phase%203%20Vapor%20Testing%20Suite.md>)
- [Phenomenon.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Phenomenon.md>)
- [Pillar Dependency Topology.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Pillar%20Dependency%20Topology.md>)
- [Player-to-Creator Path.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Player-to-Creator%20Path.md>)
- [Polycentric Pillars.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Polycentric%20Pillars.md>)
- [Portal Traversal Semantics.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Portal%20Traversal%20Semantics.md>)
- [Project Artifact Structure.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Project%20Artifact%20Structure.md>)
- [Project Authoring Structure.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Project%20Authoring%20Structure.md>)
- [Project Ethos.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Project%20Ethos.md>)
- [Project Runtime Representation.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Project%20Runtime%20Representation.md>)
- [Project Structure.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Project%20Structure.md>)
- [Redistributable Mod Contract Source.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Redistributable%20Mod%20Contract%20Source.md>)
- [Redistributable Mod Implementation Library.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Redistributable%20Mod%20Implementation%20Library.md>)
- [Reserved Built-In Mod Role.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Reserved%20Built-In%20Mod%20Role.md>)
- [Rhai Asset.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Rhai%20Asset.md>)
- [Rhai Capability.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Rhai%20Capability.md>)
- [Runtime Lock.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Runtime%20Lock.md>)
- [Runtime Substrate.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Runtime%20Substrate.md>)
- [Rust Host Contract.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Rust%20Host%20Contract.md>)
- [Rust Surface Graph.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Rust%20Surface%20Graph.md>)
- [Scale Contract.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Scale%20Contract.md>)
- [Scale Definition.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Scale%20Definition.md>)
- [Scale Realizer Cardinality.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Scale%20Realizer%20Cardinality.md>)
- [Scale Realizer.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Scale%20Realizer.md>)
- [Scale Slice.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Scale%20Slice.md>)
- [Scale Support.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Scale%20Support.md>)
- [Scale View.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Scale%20View.md>)
- [Scale.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Scale.md>)
- [Scaled Capability Channel.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Scaled%20Capability%20Channel.md>)
- [Script Safety.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Script%20Safety.md>)
- [Scriptable Rust Surface.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Scriptable%20Rust%20Surface.md>)
- [Scripting Projection Meta-Layer.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Scripting%20Projection%20Meta-Layer.md>)
- [SDK.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/SDK.md>)
- [Slot Graph Composition.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Slot%20Graph%20Composition.md>)
- [Source Artifact.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Source%20Artifact.md>)
- [Spacetime Engine.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Spacetime%20Engine.md>)
- [Steam Workshop.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Steam%20Workshop.md>)
- [steam-like-platform-contracts.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/steam-like-platform-contracts.md>)
- [Steam.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Steam.md>)
- [USF Contract.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/USF%20Contract.md>)
- [USF Definition Lifecycle.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/USF%20Definition%20Lifecycle.md>)
- [USF Instance Graph.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/USF%20Instance%20Graph.md>)
- [USF Instantiation Scripts.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/USF%20Instantiation%20Scripts.md>)
- [USF Runtime Evolution Lifecycle.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/USF%20Runtime%20Evolution%20Lifecycle.md>)
- [USF Runtime.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/USF%20Runtime.md>)
- [USF.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/USF.md>)
- [Vapor Crate Topology.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Vapor%20Crate%20Topology.md>)
- [Vapor Ecosystem.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Vapor%20Ecosystem.md>)
- [Vapor Launcher.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Vapor%20Launcher.md>)
- [Vapor Product Instance Stack.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Vapor%20Product%20Instance%20Stack.md>)
- [Vapor Product Stack.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Vapor%20Product%20Stack.md>)
- [Vapor Toolchain Envelope.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Vapor%20Toolchain%20Envelope.md>)
- [Vapor.lock.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Vapor.lock.md>)
- [Vapor.toml.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Vapor.toml.md>)
- [Workflow Framework.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Workflow%20Framework.md>)
- [Zone-Era Concepts.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/glossary/Zone-Era%20Concepts.md>)

### Technical glossary source files

- [Capability Dependency Layer Notes.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/tech_glossary/Capability%20Dependency%20Layer%20Notes.md>)
- [Capability Role and State Authority Notes.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/tech_glossary/Capability%20Role%20and%20State%20Authority%20Notes.md>)
- [Composite Workflow Runtime Notes.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/tech_glossary/Composite%20Workflow%20Runtime%20Notes.md>)
- [Normal Workflow Runtime Notes.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/tech_glossary/Normal%20Workflow%20Runtime%20Notes.md>)
- [README.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/tech_glossary/README.md>)
- [Rhai Bridge Domains and Access Provider Notes.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/tech_glossary/Rhai%20Bridge%20Domains%20and%20Access%20Provider%20Notes.md>)
- [Rhai Generic Dispatch Policy Notes.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/tech_glossary/Rhai%20Generic%20Dispatch%20Policy%20Notes.md>)
- [Rhai Reflection Macro Surface Notes.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/tech_glossary/Rhai%20Reflection%20Macro%20Surface%20Notes.md>)
- [Rhai Value Semantics and AccessCell Notes.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/tech_glossary/Rhai%20Value%20Semantics%20and%20AccessCell%20Notes.md>)
- [Runtime Intent Reconcile Commit Apply Mapping Notes.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/tech_glossary/Runtime%20Intent%20Reconcile%20Commit%20Apply%20Mapping%20Notes.md>)
- [Scale Contract Runtime Notes.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/tech_glossary/Scale%20Contract%20Runtime%20Notes.md>)
- [Stage Buffer Runtime Notes.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/tech_glossary/Stage%20Buffer%20Runtime%20Notes.md>)
- [Stage Sender Cache Runtime Notes.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/tech_glossary/Stage%20Sender%20Cache%20Runtime%20Notes.md>)
- [USF Contract Runtime Boundary Notes.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/tech_glossary/USF%20Contract%20Runtime%20Boundary%20Notes.md>)
- [USF Instantiation Capability Slot Notes.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/tech_glossary/USF%20Instantiation%20Capability%20Slot%20Notes.md>)
- [USF Math Raw Model Foundation Notes.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/tech_glossary/USF%20Math%20Raw%20Model%20Foundation%20Notes.md>)
- [USF Position Stack and Overflow Policy Notes.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/tech_glossary/USF%20Position%20Stack%20and%20Overflow%20Policy%20Notes.md>)
- [USF Runtime Evolution Lifecycle Notes.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/tech_glossary/USF%20Runtime%20Evolution%20Lifecycle%20Notes.md>)
- [Workflow Framework Premise Notes.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/tech_glossary/Workflow%20Framework%20Premise%20Notes.md>)
- [Workflow Instance Runtime Notes.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/tech_glossary/Workflow%20Instance%20Runtime%20Notes.md>)
- [Workflow Invariant Ledger Notes.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/tech_glossary/Workflow%20Invariant%20Ledger%20Notes.md>)
- [Workflow Runtime Structure Notes.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/tech_glossary/Workflow%20Runtime%20Structure%20Notes.md>)
- [Workflow Stage Runtime Notes.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/tech_glossary/Workflow%20Stage%20Runtime%20Notes.md>)
- [Workflow Stage Type Runtime Notes.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/tech_glossary/Workflow%20Stage%20Type%20Runtime%20Notes.md>)
- [Workflow State Runtime Notes.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/tech_glossary/Workflow%20State%20Runtime%20Notes.md>)
- [Workflow Type Request and Timeout Notes.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/tech_glossary/Workflow%20Type%20Request%20and%20Timeout%20Notes.md>)
- [Workflow Usage Patterns Legacy Notes.md](</home/leslieghf/Vapor/Vapor-Client/docs/planning-intake/source-corpus/tech_glossary/Workflow%20Usage%20Patterns%20Legacy%20Notes.md>)
