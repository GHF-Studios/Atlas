+++
id = "atlas-generator"
kind = "topic"
title = "Atlas validation and static-site generator"
summary = "A standard-library Python tool validates records, builds HTML and JSON, and serves a local preview."
claim_status = "source-verified"
parent = "atlas"
sources = ["tools/atlas.py", "tests/test_atlas.py"]
+++

`tools/atlas.py` is a dependency-free Python command-line tool. It reads `atlas.toml` and typed Markdown records, validates the data, and can build or locally serve the site.

The generator writes HTML pages, copies browser assets, and emits `atlas.json`. The JSON file has a versioned record list and a derived normalized graph projection. Authored Markdown and TOML remain authoritative; generated HTML and JSON are read models.

The Markdown renderer intentionally supports a small subset and escapes raw HTML. The tool uses Python’s standard library rather than a web framework or third-party Markdown package. The test suite covers record validation, date selection, HTML escaping, loading, and a generated-site smoke path.

This is the current implementation, not a commitment that Python or the current renderer is the permanent technology choice.
