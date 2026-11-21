# Ecosystem

This section maps how our products, tools, content, services, and people connect—and where their responsibilities end. It distinguishes working paths from intended ones; source repositories remain authoritative for implementation details.

## Contents

<pre>
├── <a href="01-overview/README.md">01-overview/</a> — What this section covers
├── <a href="02-current-state/README.md">02-current-state/</a> — What exists today
├── <a href="03-product-map/README.md">03-product-map/</a> — Products, tools, and services
├── <a href="04-product-relationships/README.md">04-product-relationships/</a> — How those parts relate
├── <a href="05-content-model/README.md">05-content-model/</a> — What moves through the ecosystem
├── <a href="06-capability-map/README.md">06-capability-map/</a> — Capabilities across its parts
├── <a href="07-system-boundaries/README.md">07-system-boundaries/</a> — Where responsibilities begin and end
├── <a href="08-authority-and-ownership/README.md">08-authority-and-ownership/</a> — Who controls what
├── <a href="09-integration-points/README.md">09-integration-points/</a> — Where systems meet
├── <a href="10-integrations/README.md">10-integrations/</a> — Connections to other systems
│   ├── <a href="10-integrations/development-tools/README.md">development-tools/</a> — Development tooling
│   ├── <a href="10-integrations/external-games/README.md">external-games/</a> — External games
│   ├── <a href="10-integrations/external-services/README.md">external-services/</a> — External services
│   └── <a href="10-integrations/steam/README.md">steam/</a> — Steam distribution
├── <a href="11-interoperability/README.md">11-interoperability/</a> — Cross-system compatibility
├── <a href="12-ecosystem-lifecycle/README.md">12-ecosystem-lifecycle/</a> — How participation and products change over time
├── <a href="13-acquisition-and-distribution/README.md">13-acquisition-and-distribution/</a> — How people find and receive products
├── <a href="14-people-and-roles/README.md">14-people-and-roles/</a> — People involved and their roles
│   ├── <a href="14-people-and-roles/audiences-and-accessibility/README.md">audiences-and-accessibility/</a> — Audiences and access needs
│   ├── <a href="14-people-and-roles/contributors/README.md">contributors/</a> — Contributors
│   ├── <a href="14-people-and-roles/creators/README.md">creators/</a> — Creators
│   ├── <a href="14-people-and-roles/developers/README.md">developers/</a> — Developers
│   ├── <a href="14-people-and-roles/operators/README.md">operators/</a> — Operators
│   └── <a href="14-people-and-roles/players/README.md">players/</a> — Players
├── <a href="15-journeys/README.md">15-journeys/</a> — Paths through the ecosystem
│   ├── <a href="15-journeys/build-to-distribute/README.md">build-to-distribute/</a> — Build to distribution
│   ├── <a href="15-journeys/create-to-publish/README.md">create-to-publish/</a> — Create to publication
│   ├── <a href="15-journeys/discover-to-play/README.md">discover-to-play/</a> — Discovery to play
│   ├── <a href="15-journeys/play-to-create/README.md">play-to-create/</a> — Play to creation
│   └── <a href="15-journeys/report-to-improve/README.md">report-to-improve/</a> — Report to improvement
├── <a href="16-community/README.md">16-community/</a> — Community and creators
│   ├── <a href="16-community/community-current-state/README.md">community-current-state/</a> — Community today
│   ├── <a href="16-community/community-vision/README.md">community-vision/</a> — Community direction
│   ├── <a href="16-community/creator-economy/README.md">creator-economy/</a> — Creator economy
│   ├── <a href="16-community/moderation-and-safety/README.md">moderation-and-safety/</a> — Safety and moderation
│   ├── <a href="16-community/openness-and-licensing/README.md">openness-and-licensing/</a> — Openness and licensing
│   └── <a href="16-community/participation/README.md">participation/</a> — Ways to participate
├── <a href="17-opportunities/README.md">17-opportunities/</a> — Possible future openings
├── <a href="18-non-goals/README.md">18-non-goals/</a> — What this section does not cover
└── <a href="19-open-questions/README.md">19-open-questions/</a> — Unresolved ecosystem questions
</pre>

## Current state — 2026-11-21

Our first-party work is connected, but it is not one finished platform or an established third-party ecosystem:

- **Vapor** is our evolving glue and tooling; the **Spacetime Engine** is a more bounded engine concept; **Loo Cast** is the game intended to use it. Atlas records how we understand this work and its relationships.
- Current repositories show Loo-Cast content being validated and packaged through Vapor tooling, with a Steam depot preview path. A preview is not a publication; actual release remains a separate action.
- Platform services and Registry have distinct service and authority roles. Product boundaries and distribution workflows are still changing.
- Public source repositories alone do not establish an external creator ecosystem or community.
