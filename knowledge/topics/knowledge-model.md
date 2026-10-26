+++
id = "knowledge-model"
kind = "topic"
title = "How Atlas organizes knowledge"
claim_status = "owner-directed"
parent = "atlas"
+++

The primary structure is a navigable graph of typed records. Questions, decisions, evidence, topics, events, and workstreams can refer to one another. Parentage and relation entries become directed edges. Search filters records by kind; Connections traverses edges by focused record, relation type, and direction; each record page exposes its local links. Atlas does not yet draw a spatial graph, and its relation labels have not yet been formalized or validated.

Dates are optional attributes. A timeline is generated from dated event records, while undated questions, decisions, and evidence remain searchable and traversable in Connections. The knowledge model is broader than its timeline view.

The current fields and labels are visible in `atlas.toml` and enforced only where the validator implements a check. They are a working bootstrap, not a finalized ontology. In particular, one `claim_status` field currently combines labels about where a claim came from (such as owner direction or source checking) with labels about whether it is settled (such as proposed or unresolved). Relation types are free-form strings rather than a validated vocabulary. Those are known modeling questions, not properties to assume away.

The timeline can show only dates that an event record explicitly carries. Atlas does not yet define a complete representation for the present state, historical validity ranges, or future intent. These distinctions are tracked as separate questions so decisions about them can be answered without treating chronology as the whole data model.

