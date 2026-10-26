# Atlas self-description and reviewable entrypoint

## Intent

Atlas is the canonical, durable knowledge source for GHF Studios. Its first
release should explain its own purpose and structure before importing the
large Loo-Cast/Vapor corpus. Leslie should be able to open one homepage and
judge whether the system explains itself clearly enough to continue.

## Owner-directed boundaries

- The source of truth lives in the GitHub repository `GHF-Studios/Atlas`.
- The website is a generated, replaceable view of that source.
- Questions, decisions, evidence, and workstreams form the navigable
  knowledge structure. The timeline is a generated view over dated records,
  not the database's organizing axis.
- The existing Loo-Cast/Vapor audit and its goal are preserved as a clearly
  labeled, unreviewed snapshot. Its counters remain distinct and qualified;
  reach is not semantic completion.
- This slice explains Atlas and preserves the audit. It does not ingest or
  reconcile the rest of the ecosystem's knowledge.

## Bootstrap implementation choice

Use Markdown records with a TOML metadata block. A small standard-library
Python tool validates identities and typed links, then builds a static site
and a machine-readable JSON export. This keeps authoring inspectable and
portable, without introducing a database, service, frontend framework, or
runtime dependency before the model earns one.

The initial record kinds are `topic`, `question`, `decision`, `evidence`,
`event`, and `workstream`. This is a bootstrap vocabulary, not a permanent
content-type decision. Records have stable IDs, an explicit claim/evidence
status, optional parentage, typed relations, and optional dates. Hierarchy
and chronology remain independent: only dated events populate the timeline.

## Entry experience

The home page answers, in order: what Atlas is; how to navigate it; what is
known versus proposed or unknown; what exists in this bootstrap; and what
Leslie should review next. The graph/map and timeline are separate views.
Every generated record page shows its type, claim status, relationships,
source references, and source Markdown location. A compact local search and
`atlas.json` provide human and machine entrypoints.

## Evidence rules

Owner direction, source-verified facts, reported behavior, inference,
proposal, and unresolved questions must not be presented as interchangeable
claims. A validated link proves that a target exists, not that the claim is
true. The site must say that the initial audit snapshot is not a completed or
owner-reviewed account. It must never infer dates absent from the sources.

## Alternatives considered

- Timeline-first data was set aside because it would force questions and
  decisions into chronology instead of preserving their independent
  relationships.
- A wiki-first or database-backed app was set aside for the bootstrap: it
  would add storage and editing machinery before Atlas has proven its model.
- Importing the full audit as canonical knowledge was set aside until Leslie
  reviews the self-description and can guide reconciliation.

## Scope and non-goals

Build a self-describing source tree, validator, static site, JSON export,
automated validation/deployment, and preserve the current audit snapshot
plus a durable record of the paused audit goal. Do not claim that the
snapshot is fully reconciled. Do not change source repositories, ingest
their code/docs as canonical records, create a complete questionnaire, build
books/learning paths, or introduce a write-capable web editor.

## Review gate

The first review is the generated homepage and the small set of sample
records. After Leslie approves the explanation and corrects its emphasis,
the next slice can reconcile and import broader knowledge. The provisional
record vocabulary and relationships remain open to revision at that gate.
