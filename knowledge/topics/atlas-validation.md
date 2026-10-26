+++
id = "atlas-validation"
kind = "topic"
title = "What Atlas validation does and does not establish"
summary = "Automated checks establish structural validity, not truth, owner approval, or human-facing clarity."
claim_status = "source-verified"
parent = "atlas"
sources = ["tools/atlas.py", "tests/test_atlas.py"]
+++

The current validator checks that records parse, IDs are unique and well formed, kinds match their directories, claim statuses are configured, date values are valid, parent and relation targets exist, parent links are acyclic, and cited repository paths stay inside the repository and exist.

The tests exercise representative structural failures and the static build path. The GitHub Actions workflow also checks JavaScript syntax and runs validation and site generation before publishing.

Passing these checks means the current machine-checkable constraints passed. It does **not** prove that a claim is factually correct, that an owner approved it, that the information architecture is useful, or that a human-facing page is clear. Those need evidence and review beyond code validation.
