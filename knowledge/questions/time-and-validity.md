+++
id = "time-and-validity"
kind = "question"
title = "How should Atlas represent past, present, and future?"
summary = "An event date is not the same as when a statement is valid or when a plan is intended. Decide how those temporal meanings relate."
claim_status = "unresolved"
parent = "knowledge-model"
relations = [{ type = "clarifies", target = "entrypoint-review" }, { type = "shapes", target = "timeline-is-a-view" }]
sources = ["tools/atlas.py", "knowledge/decisions/timeline-is-a-view.md"]
+++

The current timeline sorts dated event records. It does not establish when a claim became true, whether it was later superseded, or the period during which a decision applied. Future intent is represented only as prose in a question or workstream; it has no independent temporal semantics.

How should Atlas distinguish an event's date, a claim's validity over time, the current state at a repository revision, and a future intention? The timeline should remain a view over knowledge, but the data needs enough meaning to support the views the owner expects.
