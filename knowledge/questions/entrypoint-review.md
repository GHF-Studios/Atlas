+++
id = "entrypoint-review"
kind = "question"
title = "Which Atlas model decisions come first?"
claim_status = "unresolved"
relations = [{ type = "about", target = "atlas" }]
parent = "knowledge-model"
+++

The connected record graph is the accepted bootstrap direction. Before adding broad knowledge, Atlas needs owner review of the questions below. They are separate because each could change the model independently; they are not an exhaustive questionnaire.

## Site and knowledge semantics

The current generated site is a disposable prototype, not an approved information architecture. Its routes mix unlike roles: Search is an action, Timeline and Structure are projections, How Atlas works is reference material, the audit archive is preserved source material, and record pages show individual objects. Their mere existence does not make them equal navigation destinations.

The current record kinds also mix unlike roles: `topic` names a subject, `event` an occurrence, `workstream` an activity, while `question`, `decision`, and `evidence` describe different ways of holding or supporting knowledge. The current `claim_status` vocabulary further mixes claim basis with resolution state. These are observed design tensions, not decisions that the model must remain this way.

Before accepting the entrypoint, decide which reader intents deserve primary destinations, which are views or contextual references, and whether record kind, claim basis, and lifecycle state need separate dimensions. Search should remain a primary destination; Questions are a Search filter, not a parallel subsystem. A generic Explore destination is not an adequate answer to the remaining navigation question.

- What should `claim_status` represent? The current list combines source basis and settlement state.
- Which relation types should exist, and which require validation or direction/cardinality rules?
- How should Atlas distinguish an event in the past, a statement true at the current revision, and intended future work?
- What source identity must a claim retain when its repository file or branch changes?
- What timeline grouping, paging, and zoom levels would help a person navigate history without forcing every record into chronology?
- What semantic roles should the Atlas entrypoint and its generated routes serve, beyond Search and the dated-event Timeline?

Keep this question bounded to Atlas's own knowledge model. It does not ask Atlas to import or redesign another product's systems.

