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

Spatial scale is the main spine for organizing the world's enormous numeric space, including chunk addressing, without requiring every operation to repeatedly calculate across the full range. The intended scale range may be continuous, while fixed integer scales provide stable buckets that Phenomenon Models bind to. A phenomenon can have models across a contiguous range of these anchors, with each model using the representation that fits its scale. When the player's active scale changes, the world can reconcile those models: retain a model that remains useful above the player's scale, aggregate detail into a coarser model, or materialize finer models. This makes scale change an explicit world-level demand rather than an independent threshold decision made by every model.

Scale is not one universal value through which every decision must route. A model's selection or use may depend on the relevant conditions for its domain: spatial and temporal scales, physical fields, societal influence, or other measures. The primary spatial and temporal scales organize where and when the world is considered; they need not dictate every phenomenon's representation or solver.

The first coherent design target may be a singleplayer world, where one player's scale drives this reconciliation. Multiplayer remains a later compatibility question: multiple players may demand different model ranges at once, and the shared-state and authority rules for that case are not yet established. This is a scope choice for developing the model, not a decision that the eventual game or Engine must be singleplayer-only.

Changing the scale at which a player acts should normally mean changing the player's in-world identity or embodiment, not literally resizing the same human. A human might act at a larger scale by boarding a ship; that ship might then operate as part of a mother ship or larger societal proxy. Camera zoom and bounded inspection tools can change what is observed without changing the player's embodied scale.

A floating-point position between integer scale anchors could provide a continuous scale coordinate for LOD and other fine-grained adjustments, while Phenomenon Models remain bound to explicit integer anchors. The quantization would then be a deeper technical foundation rather than a restriction that players experience as discrete jumps. Whether this continuous coordinate can make a twofold anchor system map cleanly onto player- and developer-friendly tenfold ranges is unresolved. With fixed twofold steps, a tenfold change is about 3.32 steps: three steps span 8× and four span 16×. A finer offset might bridge that mismatch, but it must not make model-to-scale binding ambiguous. Twofold anchors offer finer transitions; tenfold anchors offer more intuitive scale labels and ranges. Neither has been chosen, and the numeric representation for the between-anchor coordinate is also open.

Temporal scale should broadly follow spatial scale: studying galactic structure may mean billions of years passing per second, while observing atomic processes may call for extreme slowdown. Other quantities—such as temperature, electric potential, magnetic flux density, and current—may have meaningful scales of their own, but how those relate to the spatial and temporal hierarchy is still open.

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


## Framework, kernels, mechanics, and content

The engine is not one universal solver. It needs a generic framework that lets many domain-specific computational kernels solve different kinds of problems under explicit, compatible contracts. A kernel's contract would make its assumptions, required inputs, outputs, state ownership, and relationship to scale clear enough that other mechanisms can use and compose it. What belongs in that common contract remains to be discovered.

The intended layers appear to be:

1. **Framework and kernel contracts:** typed, reusable interfaces and mechanisms that define how domain kernels participate in the world. Acceleration structures and solver tricks belong behind these contracts; they should be replaceable implementation choices.
2. **Domain kernels:** concrete solvers or mechanisms for particular regimes, such as rigid-body physics, gravity, thermodynamics, optics, chemistry, electricity, magnetism, or societal dynamics. Each may need its own assumptions, inputs, and appropriate scales while still honoring the relevant framework contracts. Avian is an existing rigid-body solver that could serve as an integration example, not as the model for every domain.
3. **Gameplay mechanics:** concrete rules and interactions composed from the available domain mechanisms.
4. **Content:** typed definitions and configurations that use those mechanics to describe worlds and things in them. World-generation recipes and procedural-asset generators belong here, alongside definitions for trees, rocks, planets, buildings, vehicles, materials, and other content.

This is a proposed separation of responsibilities, not a settled API or claim that all listed domains are feasible at the desired fidelity.

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

## How this reaches the products

Spacetime Engine is where the generic world model and mechanisms are explored. Loo-Cast is the game that should expose their creative consequences. Vapor could provide the authoring, workspace, composition, and launch tools for typed content and generator definitions, while the Engine retains ownership of simulation meaning. If this direction holds, Registry and Platform may need to distinguish shareable authored definitions from regenerable runtime caches. Those are implications to investigate, not current product contracts.

Current Engine code has scale-aware spatial types and demand-driven representations, but no validated physical model across the full scale range or complete experience described here. The [Spacetime Engine vision](../../03-products/spacetime-engine/vision/README.md), [cross-scale coherence notes](../../03-products/spacetime-engine/concepts/cross-scale-coherence/README.md), [approximation and fidelity notes](../../03-products/spacetime-engine/concepts/approximation-and-fidelity/README.md), and [Engine open questions](../../03-products/spacetime-engine/open-questions/README.md) track product-specific evidence and unknowns. Loo-Cast's [vision](../../03-products/loo-cast/vision/README.md) and [navigation across scales](../../03-products/loo-cast/experience/navigation-across-scales/README.md) cover its intended use and current limits.

*Working draft from direct owner discussion, updated 2026-11-14. For historical context and its evidence limits, see the [origin and intent reconstruction](https://github.com/GHF-Studios/Atlas/blob/874a24a/archive/audit-snapshot-2026-10-26/loo-cast-vapor-origin-and-intent.md).*
