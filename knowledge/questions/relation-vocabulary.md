+++
id = "relation-vocabulary"
kind = "question"
title = "How should Atlas define and validate relations?"
summary = "Relations are currently arbitrary type-and-target links. Decide the vocabulary and any direction, cardinality, or compatibility rules."
claim_status = "unresolved"
parent = "knowledge-model"
relations = [{ type = "clarifies", target = "entrypoint-review" }]
sources = ["tools/atlas.py", "knowledge/topics/knowledge-model.md"]
+++

Records can declare relations such as `about`, `explains`, `preserves`, and `shapes`. The validator checks that each relation has a string type and an existing target, but it does not check that the type is known or that a particular relation is allowed between those record kinds.

Which relation types carry stable meaning? Should relation direction be read literally, and do any links need cardinality or kind constraints? This should be answered before Atlas relies on cross-links for automated workflows.
