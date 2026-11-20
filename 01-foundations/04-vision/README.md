# Vision

This page records the owner-stated ambition for GHF Studios and the design ideas it has begun to suggest. It is a working vision, not a claim about what current software can do or a settled engine specification.

## The ambition

GHF Studios is defined by the ambition to create the Spacetime Engine and show what a game engine can make possible. The deliberately bold version is to “solve game engines”: build a framework for worlds with extraordinary spatial range and mechanistic depth, where different kinds of play can coexist in one universe.

Loo-Cast is meant to make that ambition tangible as a game. It should show how the Engine can be used, not merely demonstrate that its code runs. The Engine is the reusable framework being explored; Loo-Cast is a major creative proof of what such a framework could enable. Neither is complete today.

## A hierarchical world

Nothing in this world model is an isolated, flat thing. Phenomena and the chunks that make up space are both hierarchical and nested. A phenomenon may have representations across a contiguous range of scales, with different structures at different levels. It need not expand into the same kind of object at every step, nor into explicit objects at all.

A tree, for example, might be represented by a graph of branches, with leaves described statistically; at finer scales, some parts could resolve into cells, compounds, and atoms. A homogeneous cobalt cube might remain a compact mathematical description at a level where its internal variation does not matter. The world schema should allow these unlike representations to coexist. Bevy/ECS can be a backend for executing parts of the world, but it does not have to define the world's fundamental ontology or force every phenomenon into one monolithic object model.

The guiding rule is to choose, for each phenomenon and context, the simplest representation that is reasonably efficient and still reasonably indistinguishable from reality at the detail that matters. That is not a demand to simulate every scale everywhere. It is a demand that representation changes preserve the relevant relationships and consequences.

REVIEWER NOTE: I don't quite like this last line yet. It, not suuuper unlike the rest of this section, kinda omits a lot important basic information imo. More on that when I address this reviewer note again lol.

## Scale, chunks, and observation

“Scale” is an umbrella concept for numerical systems that describe magnitude and context, not necessarily one concrete object or one scalar shared by every decision. The Framework should define common tools and rules for numbers and magnitudes without itself defining positions. Spatial, temporal, chemical, electrical, and other scales are distinct facets with their own meanings and responsibilities, built on the shared concept. Whether spatial and temporal scales form one paired spacetime scale or two coordinated scales remains open.

Spatial position can use hierarchical chunk context to address an enormous numeric space without repeatedly calculating a giant coordinate. A bounded local floating-point value can carry into a larger chunk context when it reaches its range; different solvers and derived representations can choose the numeric precision they need. For the Spacetime Engine, a chunk position plus a unique Phenomenon identity can provide addressability. Position and identity should remain distinguishable if a Phenomenon moves; temporal position may also need to be modeled separately from spatial position.

The intended scale range may be continuous, while fixed integer anchors provide stable buckets for Phenomenon Models. A phenomenon can have models across a contiguous range of anchors, with each model using the representation that fits its scale. When the player's active scale changes, the world can reconcile those models: retain a model that remains useful above the player's scale, aggregate detail into a coarser model, or materialize finer models. Scale selection and model use can also depend on domain-specific conditions such as field magnitudes or societal influence; spatial and temporal scales help organize where and when the world is considered but need not dictate every representation or solver.

The first coherent design target may be a singleplayer world, where one player's scale drives this reconciliation. Multiplayer remains a later compatibility question: multiple players may demand different model ranges at once, and the shared-state and authority rules for that case are not yet established. This is a scope choice for developing the model, not a decision that the eventual game or Engine must be singleplayer-only.

Changing the scale at which a player acts should normally mean changing the player's in-world identity or embodiment, not literally resizing the same human. A human might act at a larger scale by boarding a ship; that ship might then operate as part of a mother ship or larger societal proxy. Camera zoom and bounded inspection tools can change what is observed without changing the player's embodied scale.

A floating-point position between integer scale anchors could provide a continuous scale coordinate for LOD and other fine-grained adjustments, while Phenomenon Models remain bound to explicit integer anchors. The quantization would then be a deeper technical foundation rather than a restriction that players experience as discrete jumps. Whether this continuous coordinate can make a twofold anchor system map cleanly onto player- and developer-friendly tenfold ranges is unresolved. With fixed twofold steps, a tenfold change is about 3.32 steps: three steps span 8× and four span 16×. A finer offset might bridge that mismatch, but it must not make model-to-scale binding ambiguous. Twofold anchors offer finer transitions; tenfold anchors offer more intuitive scale labels and ranges. Neither has been chosen, and the numeric representation for the between-anchor coordinate is also open.

Temporal behavior may broadly follow spatial scale: studying galactic structure may mean billions of years passing per second, while observing atomic processes may call for extreme slowdown. Temperature, electric potential, magnetic flux density, societal influence, and other domains may also have scales of their own. How these distinct scale facets relate, and whether any deserve a special coordinating role, remains open.

The chunk hierarchy should concentrate detail around the player's active scale. At very large scales, one chunk and some padding may be enough to provide context. Near the player's scale, many neighboring chunks may be needed—perhaps dozens. By default, the hierarchy stops before allocating chunks at finer scales than the player is currently using. A bounded request, such as looking through a magnifying glass, could ask for finer detail in a specific region. Larger-scale phenomena should remain visible as context; ordinary distance-based LOD may simplify faraway views independently of the primary scale hierarchy if that proves necessary.

This is a desired shape for the hierarchy, not a designed chunk-selection algorithm. The exact chunk ranges, padding, integer-anchor ratio, between-anchor coordinate, and relationship between observer scale and requested detail remain to be worked out.

## Time and persistence

Time scaling is meant to make loss of fine-grained persistence a natural consequence of the simulation. At a rate of billions of years per second, it would be unreasonable to preserve every year's short-lived details exactly. A phenomenon should instead use whatever coarser or statistical representation best preserves what matters over that timespan. This is not arbitrary deletion: it is a change in the kind of state that can be meaningfully represented at that scale and rate.

One proposed implementation direction is to keep the simulation cadence roughly uniform and treat experienced time scale as a numerical parameter in the governing quantities, rather than speeding up or slowing down the timestep itself. For example, a regime slowed by a factor of ten might use effective velocities scaled down by ten. This is an idea, not a validated rule; velocity alone may not preserve the same trajectory unless acceleration and other time-dependent processes are treated consistently. How participants at different scales share time in multiplayer, and how this relates to time travel, remain open.

An initial spatial-range prototype should deliberately leave time scaling out. It can assume roughly exact persistence so that scale navigation and representation can be explored without also testing time-driven loss or aggregation of detail. That is a simplifying test assumption, not a claim that exact persistence is appropriate at every scale or timespan.

## Representations and fields

A phenomenon may use a formula, a graph, a homogeneous description, a statistical model, a probabilistic field, explicit lower-scale phenomena, or a mixture of these. A probabilistic field is one possible way to represent detail that has not been explicitly realized; it is not the same thing as a field that mediates forces or other interactions.

One proposed division is for Chunks to carry the rough background state of a region—fields such as gravity, electric potential, or magnetism—while Phenomena represent typed, meaningful excitations or residual changes that are not adequately described by those background values alone. A Phenomenon is not merely a set of correlated field values; it may be an actor with its own structure and behavior. How the two forms of state interact, and when information moves between them, remains an open contract question.

Interaction fields may be global in meaning even if they are stored sparsely. A phenomenon that produces an influence—such as a magnet or a sound source—could contribute to the relevant part of a world-spanning field, which can make room for that contribution and mediate it. Nearby operations might use scale-local coordinates to place, transform, and query the relevant support without repeatedly calculating a full-scale USF position. This is a proposed design direction; field types, influence rules, storage, and ownership have not been specified.

Scales may also declare archetypical patterns for describing extent or regimes. Localized/Aerial and Instant/Continuous are useful historical examples for spatial and temporal behavior, not a fixed two-way split the Framework should impose on every scale. Other scales may need different numbers of categories, different meanings, or continuous ranges. An [early USF prompt backup](https://github.com/GHF-Studios/Loo-Cast-Legacy/blob/7a6e534a40524f9efa23353c5e4458b6b1133588/loo_cast_legacy/documents/legacy_stuff/universal_simulation_framework_prompts_backup.txt) calls Phenomenon Models “Localized” or “Aerial” (the latter described as having ambiguous boundaries), and combines those with Instant/Continuous event types. The taxonomy is useful evidence of prior thinking, not an adopted classification.


## Framework, kernels, mechanics, and content

The Engine is not one universal solver, and it should not impose one answer on every kind of process. Its framework should let a very large family of domain-specific computational kernels—potentially thousands of distinct mechanisms working together—address different physical, chemical, subatomic, societal, planetary, cosmological, and other problems. Their detailed assumptions, representations, and fidelity targets are decided case by case. The framework makes those solutions possible to describe, integrate, and run; it does not make the domain-specific solutions disappear.

The Framework is intended to be a library of reusable tools within Vapor, not a separate product or bespoke identity. A placeholder crate name such as `vapor_game_engine_utils` illustrates the shape, not a chosen name. Vapor provides the tools to author and validate kernel contracts for Vapor-managed code; the Spacetime Engine contains the concrete runtime kernels; games and lower-level content use and configure those kernels. The shared library and kernel foundation may be substantial, but concrete domain mechanisms, gameplay rules, and content are expected to account for much more code overall.

There may be one general meta-contract describing how a domain-specific Kernel Contract is defined. That meta-contract could be implemented with library types, macros, code generation, build-time validation, or some combination; the mechanism is undecided. Each domain can then declare the contract its kernels need. A contract may describe a kernel's identity and scope; assumptions and required state; units and interpretation; events it receives and emits; world state it may read and write; supported scale facets and ranges; coupling to fields and other kernels; lifecycle and scheduling; persistence and transitions; fidelity, error, and uncertainty; resource bounds; and diagnostics. Which parts are universal guarantees, optional declarations, or domain-specific is a central design question.

A broad Vapor ecosystem premise is that code and content can expose their structure through explicit metadata and contracts. Tools can then map, organize, validate, and generate around declared structure instead of trying to infer it all or reimplement a compiler. The Framework should mostly enable domains, scales, and other Engine actors to declare their nature; its own hard invariants should be limited to what is needed for safe typing, orchestration, and management.

Solvers are expected to read events and world state from Chunks and Phenomena, then produce events and state writes. A shared lifecycle or schedule coordinates those interactions so that domain-specific solvers can overlap and combine without becoming one universal solver. The exact rules for concurrent reads, writes, ordering, and conflict resolution remain open.

When an active domain or scale has no usable handler, the Engine should represent that condition explicitly instead of silently pretending the domain had no effect. One proposal is to move the affected state into a low-cost null or errored state carrying its cause; dependent work can propagate that error until a capable adapter turns it into an in-world anomaly. If no safe representation or indicator is available, the failure may need to escalate to a hard failure or panic. This is a fault-handling direction, not a settled lifecycle contract.

The intended ownership layers appear to be:

1. **Vapor library and tooling:** the general meta-contract machinery and tools for creating and validating domain Kernel Contracts in Vapor-managed code. These tools need not define simulation behavior.
2. **Spacetime Engine:** the runtime and concrete kernels for particular regimes, such as rigid-body physics, gravity, thermodynamics, optics, chemistry, electricity, magnetism, or societal dynamics. Avian is an existing rigid-body solver that could serve as an integration example, not as the model for every domain.
3. **Game and content:** the use and composition of kernels to create gameplay mechanics and worlds. Typed definitions, world-generation recipes, and procedural-asset generators belong here, alongside definitions for trees, rocks, planets, buildings, vehicles, materials, and other content.

This is a proposed separation of responsibilities, not a settled dependency graph, API, or claim that all listed domains are feasible at the desired fidelity.

The intended authoring model is strongly typed and declarative. A script-like asset could configure a generator or build a typed model through restricted functions and safe capabilities, rather than act as an arbitrary program with broad access. Evaluating that declaration would produce data or a cached typed result for native Rust mechanisms to run. Rhai is an idea for this role, not a settled choice. Whether declarations are assimilated only before simulation starts or can be reevaluated during play/editing—and whether ECS systems can be created dynamically—remains undecided.

Procedural media belongs downstream of world state. Sounds, textures, sprites, models, and music might be generated from that state and cached when useful; localization may be an exception. The authored definition or generator and its disposable generated result are different things, even if both are called assets.

REVIEWER NOTE: Maybe call them "Asset Generators" and "Assets" and state that "Assets" are "ephemeral"?

## Progressive prototype direction

The first demonstration should test one capability at a time rather than pretend to validate the whole Engine. A possible progression is:

1. Explore a singleplayer spatial domain across an extreme numeric range—illustratively, zooming by something like 2^256—without time scaling or terrain edits. Begin by proving that navigation and coordinates can escape the ordinary f32/f64 range; keep the world to static generated geometry.
2. Add terrain rendering and hardcoded collision, then compare candidate integer scale-anchor ratios and their between-anchor behavior.
3. Add terrain editing, potentially through sparse overrides, to test whether edits remain discoverable across scale changes.
4. Introduce background fields and typed Phenomena, then test a generic kernel contract with one domain solver before adding other domains.

The order and exact boundaries are provisional. This prototype ladder is a way to pose and isolate problems; passing one stage would not establish that other physical, chemical, optical, or social regimes are solved.

## Major open questions

The first five questions are not expected to receive one universal answer. They are a repeatable case-by-case inquiry for each domain, process, or Phenomenon and its Models—potentially thousands of cases in a mature Engine:

- What are the relevant entities, fields, Phenomena, and state owners in this domain, and how do they relate?
- What spatial and temporal extents apply? Are the relevant things localized or continuous, instantaneous or extended, and how do those categories relate to scale and representation?
- Which representations and kernels fit, and what must remain invariant when detail is materialized, retained, or aggregated? What may be approximated or lost, and how is the state reconstructed?
- How does observation or a player's in-world identity create demand for this domain's detail? What do camera zoom and bounded inspection requests change, and what do they leave alone?
- What does believable behavior mean here, and what domain-specific evidence would demonstrate the chosen fidelity? How do time, lifetimes, events, causality, and persistence work in this case?

The framework-wide questions are different:

- **Scale as a shared concept:** What common numerical and metadata tools make spatial, temporal, electrical, chemical, and other scales members of one family? Which semantics must remain specific to each facet?
- **Space and time:** Are these separate coordinated scales or one spacetime scale? How do their shared numerical foundations relate to their distinct roles in addressability, chunk context, temporal position, order, and causality?
- **Scale structure and coverage:** What does a scale declaration or sparse registry record? How are supported ranges and per-scale archetypes described, and how is a missing handler distinguished from a domain that is simply inactive?
- **Vapor library and contracts:** What does the general kernel meta-contract guarantee, and how does Vapor use it to create domain-specific Kernel Contracts? Which pieces belong in reusable library types, macros, code generation, or build-time validation?
- **Metadata as a software model:** What structures must projects declare so tools can map, organize, validate, and generate around code without inferring compiler semantics? Which assumptions can safely be generalized across projects?
- **Solver lifecycle:** How are event inputs and world-state reads coordinated with state writes and emitted events? What ordering, concurrency, and conflict rules are needed for interacting kernels?
- **Error propagation:** What is the null or errored state, how does it retain and propagate causes, and which adapters may turn it into an in-world anomaly? When should failure escalate to a panic?
- **Prototype evidence:** Which progressively more capable prototypes can test the numerical foundation, contract tooling, solver coordination, and error handling without implying that untested domains are solved?

## How this reaches the products

The shared Framework tools are intended to live as a library within Vapor. Vapor owns the authoring and validation tools for domain Kernel Contracts; Spacetime Engine owns the concrete runtime kernels; Loo-Cast and other games use and configure those kernels through authored content. This keeps the contract tooling connected to Vapor's metadata-driven project model without making the Framework a separate product or making the Engine depend on Vapor's application layer. If this direction holds, Registry and Platform may need to distinguish shareable authored definitions from regenerable runtime caches. Those are implications to investigate, not current product contracts.

Current Engine code has scale-aware spatial types and demand-driven representations, but no validated physical model across the full scale range or complete experience described here. The [Spacetime Engine vision](../../03-products/spacetime-engine/vision/README.md), [cross-scale coherence notes](../../03-products/spacetime-engine/concepts/cross-scale-coherence/README.md), [approximation and fidelity notes](../../03-products/spacetime-engine/concepts/approximation-and-fidelity/README.md), and [Engine open questions](../../03-products/spacetime-engine/open-questions/README.md) track product-specific evidence and unknowns. Loo-Cast's [vision](../../03-products/loo-cast/vision/README.md) and [navigation across scales](../../03-products/loo-cast/experience/navigation-across-scales/README.md) cover its intended use and current limits.

*Working draft from direct owner discussion, updated 2026-11-17. For historical context and its evidence limits, see the [origin and intent reconstruction](https://github.com/GHF-Studios/Atlas/blob/874a24a/archive/audit-snapshot-2026-10-26/loo-cast-vapor-origin-and-intent.md).*
