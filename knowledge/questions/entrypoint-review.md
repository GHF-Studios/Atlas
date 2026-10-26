+++
id = "entrypoint-review"
kind = "question"
title = "Which Atlas model decisions remain open?"
claim_status = "unresolved"
relations = [{ type = "about", target = "atlas" }]
parent = "knowledge-model"
+++

The connected record graph is the accepted bootstrap direction. Before adding broad knowledge, Atlas needs owner review of the questions below. They are separate because each could change the model independently; they are not an exhaustive questionnaire.

## Site and knowledge semantics

The current generated site is a disposable prototype whose information architecture is being tested. Search, Connections, and Timeline are now the owner-directed primary views for lookup, relationship traversal, and chronology. How Atlas works is system reference material, the audit archive is preserved source material, and record pages show individual objects; they remain contextual rather than peer tabs.

The current record kinds also mix unlike roles: `topic` names a subject, `event` an occurrence, `workstream` an activity, while `question`, `decision`, and `evidence` describe different ways of holding or supporting knowledge. The current `claim_status` vocabulary further mixes claim basis with resolution state. These are observed design tensions, not decisions that the model must remain this way.

The navigation choice is recorded in [Connections is a primary way into Atlas](../decisions/connections-is-a-primary-view.md). Questions remain a Search filter, not a parallel subsystem, and there is no generic Explore destination. Remaining model questions are independent of that navigation decision.

- What should `claim_status` represent? The current list combines source basis and settlement state.
- Which relation types should exist, and which require validation or direction/cardinality rules?
- How should Atlas distinguish an event in the past, a statement true at the current revision, and intended future work?
- What source identity must a claim retain when its repository file or branch changes?
- What timeline grouping, paging, and zoom levels would help a person navigate history without forcing every record into chronology?

Keep this question bounded to Atlas's own knowledge model. It does not ask Atlas to import or redesign another product's systems.

