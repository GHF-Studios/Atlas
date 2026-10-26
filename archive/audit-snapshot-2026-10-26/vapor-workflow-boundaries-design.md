# Vapor workflow boundaries and local content inventory

Status: design for review; no product code changed.

## Confirmed problems

- **Conflated inventory:** `discover_content_catalog` merges authored workspace sources with cached and installed outputs. Library and Studio then filter location kinds to recover distinct meanings. Source projects therefore appear like installed/user content.
- **Blocking and duplicated discovery:** `CatalogAction::Refresh` synchronously refreshes workspace source projects, recursively scans for unregistered projects, then scans the source catalog again while assembling cache/install inventory. `DiscoverContentProjects` repeats the workspace scan. These actions run in the service dispatch path, so large source trees can make unrelated requests appear hung.
- **Globally serialized work:** the session has one `active_operation`; multiple action families reject new work with “Wait for the current operation to finish.” A slow scan/build/workshop operation can therefore block or reject unrelated user actions, rather than scheduling by conflicting resources.
- **Inconsistent experience boundaries:** Studio groups Play and Find Content separately from one broad Creator Tools group, with no visible distinction between composition authoring and source-code/content development. Launcher is player-focused, IDE opens source workspaces, and CLI exposes technical commands, but all use the same service without a shared workflow-level model.
- **Misleading role model:** `VaporRole` is an ordinal four-value enum. It both records installation/toolchain setup and is presented as the user's role. Every non-player role currently provisions the same developer environment. It is not the authorization boundary for service actions; publishing authority is separate.
- **Duplicated semantics in projections:** the service snapshot contains an installation role and a list of available actions, while individual frontends make additional navigation and workflow decisions. The API does not describe a common progressive player → composition creator → content developer surface.

## Recommended model

Treat three progressive workflow levels as nested sets of available work, not three unrelated personas or security roles:

1. **Player:** launch a selected playable composition; discover, subscribe to, install, update, repair, and remove content; inspect what is available on this device. Keep technical source projects and build internals out of this path.
2. **Composer / technical player:** everything in Player, plus create and manage playable compositions from acquired content, select dependencies, fork or customize a composition, and review its resolved contents. Composition is Rust/Cargo-backed: Vapor owns and composes the Cargo/package build wiring, and may expose the relevant composition metadata (including Cargo dependency declarations) without requiring the user to write Rust source. The managed Rust toolchain may be required to realize/build a composition.
3. **Content developer / modder:** everything in Composer, plus author and edit content source projects, write Rust and Rhai code, own source-level project/build configuration, validate and publish authored content, and work with the Superworkspace. First-party ecosystem operations remain further gated by their own authority.

These levels describe *which workflows and detail are surfaced*. They do not assert competence, identity, or permission. Do not require a user to declare a persona before using an operation they are otherwise equipped and authorized to perform. Use progressively revealed, clearly cordoned areas with contextual invitations to go deeper; preserve an obvious Player path at every level.

Keep three independent facts in the shared service model:

- **Workflow boundary:** every action is classified at Player, Composer, or Developer level and each higher level includes the lower levels. This guides progressive navigation and contextual discovery; users do not declare a persona to gain authority, and workflow level is not an access-control token.
- **Local readiness:** installed Vapor-managed tools and target support, reported per capability (for example Rust toolchain, rust-analyzer, Windows GNU linker, Tracy). Readiness enables relevant operations and drives setup/repair, but does not imply permission.
- **Authority:** Steam account, publisher, first-party, or other service authorization. The service validates it at the operation boundary. UI visibility never grants authority.

The existing four-value `VaporRole` must not be treated as this model by simple renaming. Replace or narrow its responsibility only after a migration plan: installation setup should describe the tool capabilities actually installed (Composer can require a managed Rust toolchain without exposing Rust source authoring), while workflow depth is user-facing preference and authorization is independently checked.

## Content lifecycle and ownership

Keep one canonical content identity and dependency graph, with separate projections for separate jobs:

```text
Authored project/source ──build/package──> Acquired artifact ──install──> Composition
       Developer area                         Library                 Player area
Workshop subscription/download ────────────────┘
```

- **Workspace / project view:** registered source projects and optional unregistered-project candidates. Explicitly opened or scanned by a creator; never included in the ordinary Library inventory.
- **Library view:** local, usable artifact releases and their states: acquired, installed, disabled, update available, repair needed, or locally deployed. It does not claim source checkouts are acquired runtime artifacts.
- **Workshop view:** remote catalog metadata and subscription state, linked to the same artifact identity. Subscription, downloaded availability, Library presence, and composition membership remain distinct facts shown together where useful.
- **Composition:** the selected playable packagepack and its resolved dependency graph. The active composition is one persistent selection, not a second special “default” identity.
- Manual/local content actions and Auto-Install ownership retain their existing semantics; removal is derived from whether any subscribed or installed composition still requires an artifact, plus explicit user ownership.

## Shared service and frontend responsibilities

- The Vapor Client service owns canonical identities, lifecycle state, workflow/readiness/authority facts, operation scheduling, and action validation. All frontends consume those contracts.
- The **Launcher** presents Player workflows first: selected composition, launch/setup, discovery, subscriptions, and Library. Its normal path must not expose project source or cache mechanics.
- **Studio** serves composition authors and content developers. Composition editing belongs to the Composer level; source project, code, build, and publish tooling belongs to the clearly distinguished Developer level. They may share an app shell but must not collapse into one undifferentiated “Creator Tools” bucket.
- **IDE** operates on an explicitly open source workspace and its files/language services. It is a developer surface, not another inventory or installation manager.
- **Installer** reports and changes local tool readiness, plus first-launch prerequisites. It does not define the user's identity or silently promote a user to a workflow level.
- **CLI** exposes the same semantic operations for advanced automation/recovery. Commands declare their workflow/readiness/authority requirements and return the same operation state as GUI callers.

The protocol should expose a shared workflow classification and per-action requirements, readiness, authority outcome, and reason. Frontends may choose layout and progressive disclosure; they must not reimplement domain eligibility. A direct request is validated by the service even if a frontend is stale or bypassed.

## Responsiveness and refresh behavior

- Make ordinary local Library refresh an indexed local-artifact operation. It must not recursively scan source trees or load Workshop search results.
- Make workspace source discovery an explicit creator operation, separate from Library refresh. Its recursive/unregistered scan runs as a cancellable background operation with progress, diagnostics, and a terminal result.
- Put slow Workshop, filesystem, build, and composition-resolution work on the service operation scheduler. Replace the single global active-operation lock with resource/conflict keys so independent requests can proceed or queue while mutually conflicting operations serialize. A completed progress indicator must always have a succeeded, failed, or cancelled terminal state.
- Refresh the relevant projections when an operation completes; do not make unrelated browsing wait for a workspace scan.

## Implementation sequence

1. **Semantic model:** define workflow levels, local readiness, authorization, per-action requirements, and the canonical projections. Audit every action and every frontend against them; decide the narrow persistent workflow preference and the mapping/removal plan for `VaporRole`.
2. **Inventory separation:** remove Workspace locations from Library catalog production. Expose workspace source discovery only through workspace operations. Update Launcher, Studio, CLI, composition resolution, and tests/fixtures to consume the correct projection.
3. **Operation boundary:** move catalog/workspace refresh and other demonstrated long scans off synchronous dispatch. Add operation lifecycle, cancellation, per-resource scheduling, and responsive unrelated requests.
4. **Progressive product surfaces:** reorganize navigation and common actions around the three nested workflows across Launcher, Studio, IDE, Installer, and CLI. Ensure each surface uses service-provided eligibility/readiness/authority explanations.
5. **Integration:** migrate persisted role/setup state safely, verify cross-platform startup and service contracts, and exercise end-to-end player → composition author → content developer flows.

## Acceptance criteria

- A source checkout never appears as an acquired Library item unless it has a separately realized artifact.
- Ordinary Library refresh does not traverse a source workspace; creator workspace discovery is explicit, cancellable, and observable.
- A slow scan cannot prevent an unrelated search, subscription view, or queued independent action from receiving service responses.
- A Player sees an immediate path to launch and install. A Composer can produce a playable packagepack without needing raw source tooling. A Developer sees all lower-level workflows plus source/build/publish tools, subject to actual readiness and authority.
- The same action has the same eligibility result in GUI, CLI, and direct service requests; not-ready and unauthorized states are distinct and explainable.
- No duplicated “default” composition identity or contradictory subscription/download/Library state is introduced.

## Decision needed before implementation

The Composer boundary is now grounded in the clarified direction: composition is Rust/Cargo-backed, but Rust source authoring is not required at level 2. Vapor owns the composition wiring; level 3 exposes authored Rust/Rhai source projects and related tools. The implementation should preserve that separation in naming, UI, generated files, tool requirements, and action capability contracts.
