+++
id = "source-identity"
kind = "question"
title = "What makes a source citation durable?"
summary = "A repository path can change or point to newer content. Decide what revision, locator, and provenance a claim must preserve."
claim_status = "unresolved"
parent = "knowledge-model"
relations = [{ type = "clarifies", target = "entrypoint-review" }]
sources = ["tools/atlas.py", "knowledge/topics/atlas-system.md"]
+++

Atlas records can cite repository-relative paths. Generated site links are pinned to the Atlas source revision when available, but the authored citation itself does not identify a source revision, commit, line range, external URL, or quoted passage.

What evidence locator is enough to let a future reader verify a claim after a source file changes? Should citations point to immutable commits, named versions, line ranges, source excerpts, or some combination? Keep machine-verifiable facts separate from editorial claims about what a source means.
