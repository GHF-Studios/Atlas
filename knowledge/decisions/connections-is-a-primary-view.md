+++
id = "connections-is-a-primary-view"
kind = "decision"
title = "Connections is a primary way into Atlas"
summary = "Atlas separates record lookup, relationship traversal, and chronology into Search, Connections, and Timeline."
claim_status = "owner-directed"
parent = "atlas-site"
relations = [{ type = "applies-to", target = "knowledge-model" }]
+++

Atlas has three primary reading views with different jobs:

- **Search** finds records by text and kind. Questions remain a record kind and filter here.
- **Connections** starts from records and follows their directed, typed links. It uses the current `parent` and `relations` fields and shows labels as authored. The view does not define or validate the relation vocabulary; that remains an open model question.
- **Timeline** arranges dated event records. It does not force every record into chronology.

The old parent-only Structure page is removed as a separate route. Parent links remain traversable in Connections. How Atlas works, the preserved audit, and the machine-readable export remain contextual references rather than peer knowledge tabs. There is no generic Explore destination.

This is an information-architecture decision, not a claim that the current relation model is complete or that a spatial graph visualization is needed.
