+++
id = "entrypoint-review"
kind = "question"
title = "Which Atlas model decisions come first?"
claim_status = "unresolved"
relations = [{ type = "about", target = "atlas" }]
parent = "knowledge-model"
+++

The connected record graph is the accepted bootstrap direction. Before adding broad knowledge, Atlas needs owner review of the questions below. They are separate because each could change the model independently; they are not an exhaustive questionnaire.

- What should `claim_status` represent? The current list combines source basis and settlement state.
- Which relation types should exist, and which require validation or direction/cardinality rules?
- How should Atlas distinguish an event in the past, a statement true at the current revision, and intended future work?
- What source identity must a claim retain when its repository file or branch changes?
- What timeline grouping, paging, and zoom levels would help a person navigate history without forcing every record into chronology?

Keep this question bounded to Atlas's own knowledge model. It does not ask Atlas to import or redesign another product's systems.

