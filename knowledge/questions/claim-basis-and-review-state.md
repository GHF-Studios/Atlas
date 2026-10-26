+++
id = "claim-basis-and-review-state"
kind = "question"
title = "Should claim basis and review state be separate fields?"
summary = "The current claim_status list mixes where a claim came from with whether it is settled. Decide whether Atlas models these independently."
claim_status = "unresolved"
parent = "knowledge-model"
relations = [{ type = "clarifies", target = "entrypoint-review" }]
sources = ["atlas.toml", "knowledge/topics/knowledge-model.md"]
+++

Atlas currently uses `claim_status` values including `owner-directed`, `source-verified`, `reported`, `inferred`, `proposed`, `unresolved`, and `historical-snapshot`. These do not all answer the same question: some describe a claim's basis or provenance, some describe its acceptance or resolution, and one describes the status of a preserved bundle.

Should these remain one deliberately broad editorial label, or become separate typed dimensions? If separated, what combinations are valid, and how should older records migrate? This is an open model decision; no field change is implied here.
