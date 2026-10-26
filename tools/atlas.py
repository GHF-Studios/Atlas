#!/usr/bin/env python3
"""Validate Atlas records and build a dependency-free static site."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date, datetime
from html import escape, unescape
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tomllib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import quote, unquote, urlsplit


KIND_DIRS = {
    "topic": "topics",
    "question": "questions",
    "decision": "decisions",
    "evidence": "evidence",
    "event": "events",
    "workstream": "workstreams",
}
DEFAULT_STATUSES = {
    "owner-directed",
    "source-verified",
    "reported",
    "inferred",
    "proposed",
    "unresolved",
    "historical-snapshot",
}
ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_DELIMITER = "+++"


@dataclass(frozen=True)
class Record:
    path: Path
    metadata: dict[str, Any]
    body: str

    @property
    def id(self) -> str:
        return str(self.metadata.get("id", ""))

    @property
    def kind(self) -> str:
        return str(self.metadata.get("kind", ""))

    @property
    def title(self) -> str:
        return str(self.metadata.get("title", self.id))

    @property
    def claim_status(self) -> str:
        return str(self.metadata.get("claim_status", ""))


@dataclass(frozen=True)
class ValidationError:
    code: str
    path: str
    message: str


def _toml_scalar(value: Any) -> Any:
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, list):
        return [_toml_scalar(item) for item in value]
    if isinstance(value, dict):
        return {key: _toml_scalar(item) for key, item in value.items()}
    return value


def _relative_path(path: Path, root: Path | None) -> str:
    if root is not None:
        try:
            return path.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            pass
    return path.as_posix()


def load_records(root: Path) -> tuple[list[Record], list[ValidationError]]:
    records: list[Record] = []
    errors: list[ValidationError] = []
    knowledge = root / "knowledge"
    if not knowledge.exists():
        return records, [ValidationError("missing-knowledge", "knowledge", "No knowledge/ directory exists.")]

    for path in sorted(knowledge.rglob("*.md")):
        relative = _relative_path(path, root)
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            errors.append(ValidationError("read-error", relative, str(error)))
            continue
        lines = text.splitlines()
        if not lines or lines[0].strip() != FRONTMATTER_DELIMITER:
            errors.append(ValidationError("missing-frontmatter", relative, "Expected TOML frontmatter delimited by +++ on the first line."))
            continue
        try:
            closing = lines.index(FRONTMATTER_DELIMITER, 1)
        except ValueError:
            errors.append(ValidationError("unclosed-frontmatter", relative, "TOML frontmatter has no closing +++ delimiter."))
            continue
        try:
            metadata = tomllib.loads("\n".join(lines[1:closing]))
        except tomllib.TOMLDecodeError as error:
            errors.append(ValidationError("invalid-frontmatter", relative, str(error)))
            continue
        body = "\n".join(lines[closing + 1 :]).strip()
        records.append(Record(Path(relative), metadata, body))
    return records, errors


def timeline_records(records: list[Record]) -> list[Record]:
    dated = [record for record in records if record.kind == "event" and record.metadata.get("date") is not None]
    return sorted(dated, key=lambda record: (str(_toml_scalar(record.metadata["date"])), record.id))


def validate_records(
    records: list[Record],
    *,
    root: Path | None = None,
    kinds: dict[str, str] | None = None,
    statuses: set[str] | None = None,
) -> list[ValidationError]:
    kind_dirs = kinds or KIND_DIRS
    known_statuses = statuses or DEFAULT_STATUSES
    errors: list[ValidationError] = []
    by_id: dict[str, Record] = {}

    def issue(record: Record, code: str, message: str) -> None:
        errors.append(ValidationError(code, _relative_path(record.path, root), message))

    for record in records:
        identifier = record.id
        if not identifier or not ID_PATTERN.fullmatch(identifier):
            issue(record, "invalid-id", "id must be a non-empty lowercase kebab-case identifier.")
        if identifier in by_id:
            issue(record, "duplicate-id", f"id {identifier!r} is already used by {_relative_path(by_id[identifier].path, root)}.")
        else:
            by_id[identifier] = record
        if record.kind not in kind_dirs:
            issue(record, "invalid-kind", f"kind must be one of: {', '.join(sorted(kind_dirs))}.")
        else:
            parts = PurePosixPath(_relative_path(record.path, root)).parts
            expected = ("knowledge", kind_dirs[record.kind])
            if parts[:2] != expected:
                issue(record, "kind-path-mismatch", f"{record.kind!r} records belong under knowledge/{kind_dirs[record.kind]}/.")
        if not record.title.strip():
            issue(record, "missing-title", "title must not be blank.")
        if record.claim_status not in known_statuses:
            issue(record, "invalid-claim-status", f"claim_status must be one of: {', '.join(sorted(known_statuses))}.")

        event_date = record.metadata.get("date")
        if event_date is not None:
            try:
                date.fromisoformat(str(_toml_scalar(event_date)))
            except ValueError:
                issue(record, "invalid-date", "date must use the ISO calendar date form YYYY-MM-DD.")
        if record.kind == "event" and not record.body:
            issue(record, "missing-event-description", "event records need a concise description.")

        parent = record.metadata.get("parent")
        if parent is not None and not isinstance(parent, str):
            issue(record, "invalid-parent", "parent must be a record id string.")
        relations = record.metadata.get("relations", [])
        if not isinstance(relations, list):
            issue(record, "invalid-relations", "relations must be an array of tables.")
            relations = []
        for relation in relations:
            if not isinstance(relation, dict) or not isinstance(relation.get("target"), str) or not isinstance(relation.get("type"), str):
                issue(record, "invalid-relation", "each relation needs string fields type and target.")

        sources = record.metadata.get("sources", [])
        if not isinstance(sources, list) or any(not isinstance(source, str) for source in sources):
            issue(record, "invalid-sources", "sources must be an array of repository-relative paths.")
            continue
        for source in sources:
            source_path = PurePosixPath(source)
            if source_path.is_absolute() or ".." in source_path.parts:
                issue(record, "unsafe-source-path", f"source path must stay inside the repository: {source!r}.")
            elif root is not None and not (root / Path(*source_path.parts)).is_file():
                issue(record, "missing-source", f"source file does not exist: {source!r}.")

    for record in records:
        targets: list[str] = []
        parent = record.metadata.get("parent")
        if isinstance(parent, str):
            targets.append(parent)
        for relation in record.metadata.get("relations", []) if isinstance(record.metadata.get("relations", []), list) else []:
            if isinstance(relation, dict) and isinstance(relation.get("target"), str):
                targets.append(relation["target"])
        for target in targets:
            if target not in by_id:
                issue(record, "missing-target", f"relation target {target!r} does not exist.")

    state: dict[str, int] = {}

    def visit(identifier: str, stack: list[str]) -> None:
        state[identifier] = 1
        parent = by_id[identifier].metadata.get("parent")
        if isinstance(parent, str) and parent in by_id:
            if state.get(parent) == 1:
                issue(by_id[identifier], "parent-cycle", "parent hierarchy contains a cycle: " + " -> ".join(stack + [parent]) + ".")
            elif state.get(parent, 0) == 0:
                visit(parent, stack + [parent])
        state[identifier] = 2

    for identifier in by_id:
        if state.get(identifier, 0) == 0:
            visit(identifier, [identifier])
    return errors


def _inline_markdown(text: str, link_resolver=None) -> str:
    escaped = escape(text, quote=True)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", escaped)

    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

    def link(match: re.Match[str]) -> str:
        label = match.group(1)
        target = match.group(2)
        decoded_target = unescape(target)
        if decoded_target.startswith(("https://", "http://", "mailto:", "#")):
            return f'<a href="{target}">{label}</a>'
        if link_resolver is not None:
            resolved = link_resolver(decoded_target)
            if resolved is not None:
                return f'<a href="{escape(resolved, quote=True)}">{label}</a>'
            if decoded_target.startswith("/"):
                return label
        elif decoded_target.startswith("/"):
            return f'<a href="{target}">{label}</a>'
        return label

    return link_pattern.sub(link, escaped)


def render_markdown(markdown: str, link_resolver=None) -> str:
    """Render a conservative Markdown subset; raw HTML is always escaped."""
    output: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []
    code_lines: list[str] | None = None
    heading_ids: set[str] = set()

    def heading_id(source: str) -> str:
        plain = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", source)
        plain = re.sub(r"[`*~]", "", plain).lower()
        plain = re.sub(r"[^\w -]", "", plain, flags=re.UNICODE).strip().replace(" ", "-")
        base_id = plain or "section"
        candidate = base_id
        suffix = 1
        while candidate in heading_ids:
            candidate = f"{base_id}-{suffix}"
            suffix += 1
        heading_ids.add(candidate)
        return candidate

    def flush_paragraph() -> None:
        if paragraph:
            output.append("<p>" + _inline_markdown(" ".join(part.strip() for part in paragraph), link_resolver) + "</p>")
            paragraph.clear()

    def flush_list() -> None:
        if list_items:
            output.append("<ul>" + "".join(f"<li>{_inline_markdown(item, link_resolver)}</li>" for item in list_items) + "</ul>")
            list_items.clear()

    for line in markdown.splitlines():
        if line.startswith("```"):
            flush_paragraph()
            flush_list()
            if code_lines is None:
                code_lines = []
            else:
                output.append("<pre><code>" + escape("\n".join(code_lines)) + "</code></pre>")
                code_lines = None
            continue
        if code_lines is not None:
            code_lines.append(line)
            continue
        heading = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", line)
        bullet = re.match(r"^\s*[-*]\s+(.+)$", line)
        if heading:
            flush_paragraph(); flush_list()
            level = len(heading.group(1))
            identifier = heading_id(heading.group(2))
            aliases = []
            underscore_alias = identifier.replace("-", "_")
            if underscore_alias != identifier and underscore_alias not in heading_ids:
                heading_ids.add(underscore_alias)
                aliases.append(f'<span id="{escape(underscore_alias, quote=True)}"></span>')
            output.append(f'{"".join(aliases)}<h{level} id="{escape(identifier, quote=True)}">{_inline_markdown(heading.group(2), link_resolver)}</h{level}>')
        elif bullet:
            flush_paragraph()
            list_items.append(bullet.group(1))
        elif not line.strip():
            flush_paragraph(); flush_list()
        else:
            flush_list()
            paragraph.append(line)
    flush_paragraph(); flush_list()
    if code_lines is not None:
        output.append("<pre><code>" + escape("\n".join(code_lines)) + "</code></pre>")
    return "\n".join(output)


def _base_url(value: str) -> str:
    if not value.startswith("/"):
        value = "/" + value
    return value.rstrip("/") + "/"


def _page(title: str, content: str, base: str, active: str = "") -> str:
    # The brand is the home/entrypoint. Search, Connections, and Timeline
    # serve distinct primary reading tasks; system reference remains separate.
    links = [("Search", "search.html"), ("Connections", "connections.html"), ("Timeline", "timeline.html")]
    nav = "".join(
        f'<a href="{base}{route}"{(" aria-current=\"page\"" if active == route else "")}>{label}</a>'
        for label, route in links
    )
    system_link = f'<a class="system-link" href="{base}system.html"{(" aria-current=\"page\"" if active == "system.html" else "")}>How it works</a>'
    # Search has a dedicated page with type filters. Do not repeat a partial
    # dropdown search on every route; that made search look like a utility.
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="atlas-base" content="{escape(base, quote=True)}">
  <meta name="description" content="Atlas, GHF Studios' linked record of questions, decisions, evidence, work and history.">
  <title>{escape(title)} · Atlas</title>
  <link rel="stylesheet" href="{base}assets/style.css">
  <script defer src="{base}assets/search.js"></script>
  <script defer src="{base}assets/connections.js"></script>
</head>
<body>
  <header class="site-header"><a class="brand" href="{base}index.html" aria-label="Atlas start"><span class="brand-mark">A</span><span>Atlas<small>GHF Studios · Start</small></span></a><nav aria-label="Knowledge views">{nav}</nav>{system_link}</header>
  <main>{content}</main>
  <footer><span>Atlas is generated from versioned Markdown records.</span><span><a href="{base}archive.html">Preserved audit material</a> · <a href="{base}atlas.json">Structured data</a> · <a href="https://github.com/GHF-Studios/Atlas">Source repository</a></span></footer>
</body>
</html>'''


def _record_link(record: Record, base: str) -> str:
    return f'<a href="{base}records/{escape(record.id, quote=True)}.html">{escape(record.title)}</a>'


def _record_card(record: Record, base: str) -> str:
    summary = record.metadata.get("summary")
    if not isinstance(summary, str) or not summary.strip():
        # Listing views should orient readers, not duplicate the entire record.
        summary = record.body.split("\n\n", 1)[0]
        summary = re.sub(r"[`*#]", "", summary)
        if len(summary) > 260:
            summary = summary[:257].rsplit(" ", 1)[0].rstrip(".,;:") + "…"
    excerpt = f"<p>{_inline_markdown(summary)}</p>"
    return (
        f'<article class="record-card"><div class="eyebrow">{escape(record.kind.replace("-", " ").title())} · '
        f'<span class="status">{escape(record.claim_status.replace("-", " "))}</span></div>'
        f'<h3>{_record_link(record, base)}</h3><div class="excerpt">{excerpt}</div></article>'
    )


def _record_json(record: Record, root: Path) -> dict[str, Any]:
    item = {key: _toml_scalar(value) for key, value in record.metadata.items()}
    item["path"] = _relative_path(record.path, root)
    item["body"] = record.body
    item["url"] = f"records/{record.id}.html"
    return item


def _graph_json(records: list[Record]) -> dict[str, list[dict[str, str]]]:
    """Return a normalized graph projection without changing record ownership."""
    nodes = [
        {"id": record.id, "kind": record.kind, "claim_status": record.claim_status}
        for record in sorted(records, key=lambda item: item.id)
    ]
    edges: list[dict[str, str]] = []
    for record in records:
        parent = record.metadata.get("parent")
        if isinstance(parent, str):
            edges.append({"source": record.id, "type": "parent", "target": parent})
        for relation in record.metadata.get("relations", []):
            if isinstance(relation, dict):
                edges.append({
                    "source": record.id,
                    "type": relation["type"],
                    "target": relation["target"],
                })
    return {
        "nodes": nodes,
        "edges": sorted(edges, key=lambda edge: (edge["source"], edge["type"], edge["target"])),
    }


def _source_url(path: str, revision: str | None) -> str | None:
    if revision is None:
        return None
    return "https://github.com/GHF-Studios/Atlas/blob/" + escape(revision, quote=True) + "/" + "/".join(escape(part, quote=True) for part in PurePosixPath(path).parts)


def _source_link(path: str, revision: str | None, label: str) -> str:
    url = _source_url(path, revision)
    return f'<a href="{url}">{escape(label)}</a>' if url else escape(label)


def _source_revision(root: Path, requested: str | None) -> str | None:
    if requested and re.fullmatch(r"[0-9a-f]{40,64}", requested):
        return requested
    try:
        dirty = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=normal"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
        if dirty.stdout.strip():
            return None
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    revision = result.stdout.strip()
    return revision if re.fullmatch(r"[0-9a-f]{40,64}", revision) else None


def build_site(root: Path, output: Path, base_url: str = "/", source_revision: str | None = None) -> list[ValidationError]:
    root = root.resolve()
    output = output.resolve()
    try:
        config = tomllib.loads((root / "atlas.toml").read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [ValidationError("missing-config", "atlas.toml", "Atlas configuration is missing.")]
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as error:
        return [ValidationError("invalid-config", "atlas.toml", str(error))]

    records, errors = load_records(root)
    configured_kinds = config.get("records", {}).get("kinds", list(KIND_DIRS))
    configured_statuses = set(config.get("records", {}).get("claim_statuses", DEFAULT_STATUSES))
    kind_dirs = {kind: KIND_DIRS[kind] for kind in configured_kinds if kind in KIND_DIRS}
    errors.extend(validate_records(records, root=root, kinds=kind_dirs, statuses=configured_statuses))
    if errors:
        return errors

    base = _base_url(base_url)
    revision = _source_revision(root, source_revision)
    by_id = {record.id: record for record in records}
    output.mkdir(parents=True, exist_ok=True)
    (output / "assets").mkdir(exist_ok=True)
    (output / "records").mkdir(exist_ok=True)
    shutil.copyfile(root / "site/assets/style.css", output / "assets/style.css")
    shutil.copyfile(root / "site/assets/search.js", output / "assets/search.js")
    shutil.copyfile(root / "site/assets/connections.js", output / "assets/connections.js")

    # A typed and queryable export; chronology is a projection over dated events.
    payload = {
        "schema_version": 1,
        "atlas": _toml_scalar(config.get("atlas", {})),
        "publication": _toml_scalar(config.get("publication", {})),
        "source_revision": revision,
        "graph": _graph_json(records),
        "records": [_record_json(record, root) for record in sorted(records, key=lambda item: (item.kind, item.title.casefold(), item.id))],
    }
    (output / "atlas.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    home_record_ids = ("atlas-product", "knowledge-model", "atlas-scope")
    home_records = [by_id[key] for key in home_record_ids if key in by_id]
    home = f'''<section class="hero"><p class="eyebrow">GHF STUDIOS · ATLAS</p><h1>A place to understand how the work fits together.</h1><p class="lead">Atlas connects explanations, decisions, questions, evidence, work, and dated events. It is being built to make a large body of knowledge navigable and honest about what is known.</p></section>
<section class="section"><div class="section-heading"><div><p class="eyebrow">ONE RECORD SET · THREE PRIMARY VIEWS</p><h2>Start with what you need</h2><p>Find a record, follow what it connects to, or see what happened over time.</p></div></div><div class="intro-grid"><article class="panel"><p class="eyebrow">FIND AND FILTER</p><h2>Search</h2><p>Search all records, then narrow by kind. Questions are one record type among several.</p><p><a href="{base}search.html">Search Atlas →</a></p></article><article class="panel"><p class="eyebrow">FOLLOW RELATIONSHIPS</p><h2>Connections</h2><p>Start from a record and follow its authored links to other records. Relation labels and direction are shown as entered.</p><p><a href="{base}connections.html">Explore connections →</a></p></article><article class="panel"><p class="eyebrow">DATED EVENTS</p><h2>Timeline</h2><p>See only events with authored dates. The current timeline is intentionally sparse.</p><p><a href="{base}timeline.html">View the timeline →</a></p></article></div></section>
<section class="section"><div class="section-heading"><div><p class="eyebrow">ATLAS DESCRIBES ITSELF FIRST</p><h2>What Atlas is</h2><p>The product’s purpose lives in the same linked record set Atlas is built to explain.</p></div></div><div class="cards">{''.join(_record_card(record, base) for record in home_records if record.id == "atlas-product")}</div></section>
<section class="section"><article class="panel"><p class="eyebrow">OWNER REVIEW · BEFORE BROADER IMPORT</p><h2>Review this bootstrap</h2><p>Atlas currently describes its own purpose, model, and prototype. This starting point is provisional. Broader Vapor and Loo-Cast knowledge will wait until you have reviewed the entrypoint and the open model questions.</p><p><a class="button" href="{base}records/entrypoint-review.html">Review Atlas questions →</a></p></article></section>
<aside class="notice"><strong>One source, several views.</strong> The pages above are projections over linked records, not separate stores of knowledge. Automated checks establish structure, not truth or owner approval. <a href="{base}system.html#claim-basis">How to read the labels</a>.</aside>'''
    (output / "index.html").write_text(_page("Home", home, base, "index.html"), encoding="utf-8")

    record_config = config.get("records", {})
    kind_descriptions = record_config.get("kind_descriptions", {})
    status_descriptions = record_config.get("claim_status_descriptions", {})
    kind_rows = "".join(
        f'<tr><th scope="row">{escape(kind.replace("-", " ").title())}</th><td>{escape(kind_descriptions.get(kind, "Definition not supplied."))}</td></tr>'
        for kind in record_config.get("kinds", [])
    )
    status_rows = "".join(
        f'<tr><th scope="row"><span class="status">{escape(status.replace("-", " "))}</span></th><td>{escape(status_descriptions.get(status, "Definition not supplied."))}</td></tr>'
        for status in record_config.get("claim_statuses", [])
    )
    guide = f'''<section class="section guide-grid" id="record-model"><article class="panel"><h2>Record types <small>bootstrap vocabulary</small></h2><table><tbody>{kind_rows}</tbody></table></article><article class="panel" id="claim-status"><h2>Claim status <small>basis and review labels</small></h2><table><tbody>{status_rows}</tbody></table></article></section>'''

    kind_buttons = ''.join(
        f'<button type="button" role="tab" id="kind-{escape(kind, quote=True)}" aria-controls="atlas-search-results" aria-selected="false" tabindex="-1" data-kind="{escape(kind, quote=True)}">{escape({"topic": "Topics", "question": "Questions", "decision": "Decisions", "evidence": "Evidence", "event": "Events", "workstream": "Workstreams"}.get(kind, kind.replace("-", " ").title()))}</button>'
        for kind in configured_kinds
    )
    search_body = f'''<section class="page-intro"><p class="eyebrow">KNOWLEDGE · SEARCH</p><h1>Search</h1><p>Search every record, then filter by its kind. Questions are one record type among several, not a separate knowledge system.</p><p><a href="{base}system.html#record-model">What do these record types mean?</a></p></section>
<section class="search-page" aria-label="Search Atlas records"><label for="atlas-search">Search titles and record text</label><input id="atlas-search" type="search" placeholder="Try a topic, question, decision, or source…" autocomplete="off"><div class="search-subtabs" role="tablist" aria-label="Filter by record type"><button type="button" role="tab" id="kind-all" aria-controls="atlas-search-results" aria-selected="true" tabindex="0" data-kind="all">All records</button>{kind_buttons}</div><p id="atlas-search-count" class="search-count" aria-live="polite">Loading records…</p><div id="atlas-search-results" role="tabpanel" aria-labelledby="kind-all" aria-live="polite"></div></section>'''
    (output / "search.html").write_text(_page("Search", search_body, base, "search.html"), encoding="utf-8")

    system_sections = [
        ("Product and model", ("atlas-product", "atlas-system", "knowledge-model", "timeline-is-a-view", "connections-is-a-primary-view", "current-site-is-disposable-bootstrap")),
        ("Authored data and generation", ("atlas-authoring", "atlas-generator", "atlas-validation")),
        ("Published experience", ("atlas-site", "atlas-search-and-export", "atlas-publishing")),
        ("Boundaries and open design", ("atlas-scope", "entrypoint-review")),
    ]
    system_html = '<section class="page-intro"><p class="eyebrow">SYSTEM REFERENCE · FOR AUTHORS AND MAINTAINERS</p><h1>How Atlas works</h1><p>This is the system reference: how records are authored, checked, connected, generated, and published. For Atlas’s purpose and intended role, start on the <a href="' + base + 'index.html">Atlas home</a>.</p><p><a class="button" href="#authored-data">Start at the records</a> <a class="button" href="#published-view">Follow the generated views</a></p></section>'
    for heading, identifiers in system_sections:
        section_records = [by_id[identifier] for identifier in identifiers if identifier in by_id]
        if section_records:
            anchor = "authored-data" if heading == "Authored data and generation" else "published-view" if heading == "Published experience" else "product-model" if heading == "Product and model" else "boundaries"
            system_html += f'<section class="section" id="{anchor}"><h2>{escape(heading)}</h2><div class="cards">{"".join(_record_card(record, base) for record in section_records)}</div></section>'
    system_html += '<section class="section"><h2>Current record model</h2><p>This compact table documents the filters exposed in Search. It describes the bootstrap vocabulary, not a finalized ontology.</p>' + guide + '</section>'
    system_html += '<section class="section" id="claim-basis"><h2>How to read a claim label</h2><p>A label records the kind of basis attached to a claim. It is not a universal confidence score, and passing structural checks does not make a claim true. The status definitions are in the <a href="' + base + 'system.html#claim-status">record model table</a>.</p></section>'
    (output / "system.html").write_text(_page("How Atlas works", system_html, base, "system.html"), encoding="utf-8")

    graph = _graph_json(records)
    relation_types = sorted({edge["type"] for edge in graph["edges"]})
    record_options = "".join(
        f'<option value="{escape(record.id, quote=True)}">{escape(record.title)} · {escape(record.kind)}</option>'
        for record in sorted(records, key=lambda item: (item.title.casefold(), item.id))
    )
    relation_options = "".join(
        f'<option value="{escape(relation_type, quote=True)}">{escape(relation_type)}</option>'
        for relation_type in relation_types
    )
    connection_rows = []
    for edge in graph["edges"]:
        source = by_id[edge["source"]]
        target = by_id[edge["target"]]
        source_focus = f'{base}connections.html?record={escape(source.id, quote=True)}'
        target_focus = f'{base}connections.html?record={escape(target.id, quote=True)}'
        connection_rows.append(
            f'<li class="connection-row" data-source-id="{escape(source.id, quote=True)}" '
            f'data-target-id="{escape(target.id, quote=True)}" data-relation-type="{escape(edge["type"], quote=True)}">'
            f'<div class="connection-edge"><span class="connection-node"><a href="{base}records/{escape(source.id, quote=True)}.html">{escape(source.title)}</a>'
            f'<small>{escape(source.kind)}</small></span><span class="relation" aria-label="authored relation">{escape(edge["type"])}</span>'
            f'<span class="connection-arrow" aria-hidden="true">→</span><span class="connection-node"><a href="{base}records/{escape(target.id, quote=True)}.html">{escape(target.title)}</a>'
            f'<small>{escape(target.kind)}</small></span></div><div class="connection-actions">'
            f'<a href="{source_focus}">Focus {escape(source.title)}</a><a href="{target_focus}">Focus {escape(target.title)}</a></div></li>'
        )
    connections_body = f'''<section class="page-intro"><p class="eyebrow">KNOWLEDGE · CONNECTIONS</p><h1>Connections</h1><p>Start from a record and follow its links. Each arrow follows the direction authored in Atlas, including parent links; relation labels are displayed as written and do not imply that the vocabulary is finalized.</p></section>
<section class="connection-controls panel" aria-label="Filter connections"><label for="connection-record">Focus on a record</label><select id="connection-record"><option value="">All records</option>{record_options}</select><label for="connection-type">Relation type</label><select id="connection-type"><option value="">All relation types</option>{relation_options}</select><label for="connection-direction">Direction from focused record</label><select id="connection-direction"><option value="both">Both directions</option><option value="outgoing">Outgoing</option><option value="incoming">Incoming</option></select><p id="connection-count" class="search-count" role="status">{len(connection_rows)} {"link" if len(connection_rows) == 1 else "links"}</p></section>
<p id="connection-empty" class="empty-state" hidden>No links match these filters. Try another record or relation type.</p><ul id="connection-results" class="connection-list" aria-label="Record relationships">{"".join(connection_rows)}</ul>'''
    (output / "connections.html").write_text(_page("Connections", connections_body, base, "connections.html"), encoding="utf-8")

    events = timeline_records(records)
    if events:
        timeline_body = f'<section class="page-intro"><p class="eyebrow">DATED EVENTS · {len(events)} RECORDED</p><h1>Timeline</h1><p>This view contains only events with dates. It is generated from event records and remains independent of record relationships.</p></section><ol class="timeline">'
        timeline_body += "".join(f'<li><time datetime="{escape(str(_toml_scalar(event.metadata["date"])), quote=True)}">{escape(str(_toml_scalar(event.metadata["date"])))}</time>{_record_card(event, base)}</li>' for event in events)
        timeline_body += "</ol>"
    else:
        timeline_body = '<section class="page-intro"><p class="eyebrow">DATED EVENTS · 0 RECORDED</p><h1>Timeline</h1></section><div class="empty-state"><h2>No dated events</h2><p>Undated knowledge remains searchable and structured. Atlas does not invent dates to fill this view.</p></div>'
    timeline_body += '<section class="section"><h2>Timeline boundary</h2><p>This page contains normalized Atlas event records only. The preserved audit contains a separate historical reconstruction; it is source material, not a timeline dataset. <a href="' + base + 'archive.html">Open the preserved audit archive</a>.</p></section>'
    (output / "timeline.html").write_text(_page("Timeline", timeline_body, base, "timeline.html"), encoding="utf-8")

    archive_relative = PurePosixPath("archive/audit-snapshot-2026-10-26")
    archive_dir = root.joinpath(*archive_relative.parts)
    archive_items = sorted(path for path in archive_dir.rglob("*") if path.is_file())
    archive_site_dir = output.joinpath(*archive_relative.parts)
    archive_read_dir = output / "archive/read"
    if archive_site_dir.exists():
        shutil.rmtree(archive_site_dir)
    if archive_read_dir.exists():
        shutil.rmtree(archive_read_dir)
    shutil.copytree(archive_dir, archive_site_dir)
    archive_read_dir.mkdir(parents=True, exist_ok=True)

    def archive_urls(path: Path) -> tuple[str, str]:
        relative = path.relative_to(archive_dir).as_posix()
        encoded = quote(relative, safe="/")
        raw_url = base + archive_relative.as_posix() + "/" + encoded
        page_url = base + "archive/read/" + quote(relative + ".html", safe="/")
        return raw_url, page_url

    def resolve_archive_link(source: Path, target: str) -> str | None:
        parsed = urlsplit(target)
        candidate = (source.parent / unquote(parsed.path)).resolve()
        try:
            relative = candidate.relative_to(archive_dir.resolve())
        except ValueError:
            return None
        if not candidate.is_file():
            return None
        if candidate.suffix.lower() == ".md":
            destination = base + "archive/read/" + quote(relative.as_posix() + ".html", safe="/")
        else:
            destination = base + archive_relative.as_posix() + "/" + quote(relative.as_posix(), safe="/")
        return destination + ("#" + quote(parsed.fragment, safe="-._~") if parsed.fragment else "")

    archive_links: list[str] = []
    for path in archive_items:
        relative = path.relative_to(archive_dir).as_posix()
        raw_url, page_url = archive_urls(path)
        if path.suffix.lower() == ".md":
            label = f'<a href="{page_url}">{escape(relative)}</a> <a class="source-path" href="{raw_url}">download original</a>'
            archive_links.append(f"<li>{label}</li>")
            source_url = _source_url(_relative_path(path, root), revision)
            source_link = f' · <a href="{source_url}">Versioned GitHub source</a>' if source_url else ""
            page_body = f'''<section class="page-intro"><p class="eyebrow">PRESERVED AUDIT · {escape(relative)}</p><h1>{escape(path.stem.replace("-", " ").title())}</h1><p><a href="{base}archive.html">← Preserved audit bundle</a> · <a class="button" href="{raw_url}">Download original</a>{source_link}</p></section><article class="record-body">{render_markdown(path.read_text(encoding="utf-8"), lambda target, source=path: resolve_archive_link(source, target))}</article>'''
            page_path = archive_read_dir / (relative + ".html")
            page_path.parent.mkdir(parents=True, exist_ok=True)
            page_path.write_text(_page(path.name, page_body, base), encoding="utf-8")
        else:
            archive_links.append(f'<li><a href="{raw_url}">{escape(relative)}</a></li>')
    archive_readme = base + "archive/read/README.md.html"
    archive_manifest = base + "archive/read/PRESERVATION.md.html"
    archive_source_url = "https://github.com/GHF-Studios/Atlas/tree/" + revision + "/" + archive_relative.as_posix() if revision else None
    archive_source_link = f'<a href="{escape(archive_source_url, quote=True)}">Versioned GitHub snapshot</a>' if archive_source_url else ""
    archive_body = f'''<section class="page-intro"><p class="eyebrow">HISTORICAL WORKING MATERIAL</p><h1>Preserved audit bundle</h1><p>This is the earlier Loo-Cast/Vapor audit and timeline work, preserved before Atlas implementation. It is not an approved knowledge model, a complete audit, or a statement that every historical claim is current.</p><p><a class="button" href="{archive_readme}">Read the bundle guide</a> <a class="button" href="{archive_manifest}">File-by-file preservation manifest</a></p><p>Read the preserved files here in Atlas; the originals remain downloadable. {archive_source_link}</p></section><section class="section"><h2>Browse files <small>{len(archive_items)}</small></h2><ul class="file-list">{"".join(archive_links)}</ul></section>'''
    (output / "archive.html").write_text(_page("Preserved audit", archive_body, base, "archive.html"), encoding="utf-8")

    for record in records:
        details = [f'<span class="badge">{escape(record.kind)}</span>', f'<span class="badge status">{escape(record.claim_status)}</span>']
        if record.metadata.get("date") is not None:
            details.append(f'<time class="badge" datetime="{escape(str(_toml_scalar(record.metadata["date"])), quote=True)}">{escape(str(_toml_scalar(record.metadata["date"])))}</time>')
        parent_id = record.metadata.get("parent")
        parent = f'<p><strong>Parent:</strong> {_record_link(by_id[parent_id], base)}</p>' if parent_id in by_id else ""
        relations = record.metadata.get("relations", [])
        relation_html = "".join(f'<li><span class="relation">{escape(rel["type"])}</span> → {_record_link(by_id[rel["target"]], base)}</li>' for rel in relations)
        inbound = []
        for other in records:
            if other.id == record.id:
                continue
            if other.metadata.get("parent") == record.id:
                inbound.append(f'<li><span class="relation">contains</span> → {_record_link(other, base)}</li>')
            for relation in other.metadata.get("relations", []):
                if relation.get("target") == record.id:
                    inbound.append(f'<li><span class="relation">{escape(relation["type"])}</span> ← {_record_link(other, base)}</li>')
        source_html = "".join(f'<li>{_source_link(source, revision, source)}</li>' for source in record.metadata.get("sources", []))
        record_path = _relative_path(record.path, root)
        record_source_url = _source_url(record_path, revision)
        authored_at = _source_link(record_path, revision, record_path) if record_source_url else f'{escape(record_path)} <span class="status">(working tree; no fixed Git revision)</span>'
        connections = relation_html + "".join(inbound)
        record_body = f'''<section class="page-intro"><p class="eyebrow">{escape(record.kind.replace('-', ' ').upper())} · {escape(record.id)}</p><h1>{escape(record.title)}</h1><div class="badges">{"".join(details)}</div></section><article class="record-body">{render_markdown(record.body)}</article><section class="section"><h2>Connections</h2><p><a href="{base}connections.html?record={escape(record.id, quote=True)}">Open the Connections view focused on this record →</a></p>{parent}<ul>{connections or '<li>No linked records yet.</li>'}</ul></section><section class="section"><h2>Sources</h2><ul>{source_html or '<li>No source path listed.</li>'}</ul><p class="source-path">Authored at {authored_at}</p></section>'''
        (output / "records" / f"{record.id}.html").write_text(_page(record.title, record_body, base), encoding="utf-8")
    return []


def _config_values(root: Path) -> tuple[dict[str, str], list[str], list[str]]:
    config = tomllib.loads((root / "atlas.toml").read_text(encoding="utf-8"))
    records = config.get("records", {})
    return config.get("atlas", {}), records.get("kinds", list(KIND_DIRS)), records.get("claim_statuses", sorted(DEFAULT_STATUSES))


def validate(root: Path) -> list[ValidationError]:
    try:
        metadata, kinds, statuses = _config_values(root)
        del metadata
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as error:
        return [ValidationError("invalid-config", "atlas.toml", str(error))]
    records, errors = load_records(root)
    kind_dirs = {kind: KIND_DIRS[kind] for kind in kinds if kind in KIND_DIRS}
    errors.extend(validate_records(records, root=root, kinds=kind_dirs, statuses=set(statuses)))
    return errors


def _print_errors(errors: list[ValidationError]) -> None:
    for error in errors:
        print(f"{error.path}: {error.code}: {error.message}", file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate_parser = subparsers.add_parser("validate", help="validate Atlas source records")
    validate_parser.add_argument("--root", type=Path, default=Path.cwd())
    build_parser = subparsers.add_parser("build", help="build the static Atlas site and JSON export")
    build_parser.add_argument("--root", type=Path, default=Path.cwd())
    build_parser.add_argument("--output", type=Path, default=Path("dist"))
    build_parser.add_argument("--base-url", default=None, help="site base path (defaults to atlas.toml publication.base_path)")
    build_parser.add_argument("--source-revision", default=os.environ.get("GITHUB_SHA"), help="Git revision used for source links (defaults to current HEAD)")
    serve_parser = subparsers.add_parser("serve", help="build and serve Atlas locally")
    serve_parser.add_argument("--root", type=Path, default=Path.cwd())
    serve_parser.add_argument("--output", type=Path, default=Path("dist"))
    serve_parser.add_argument("--base-url", default="/")
    serve_parser.add_argument("--source-revision", default=os.environ.get("GITHUB_SHA"), help="Git revision used for source links (defaults to current HEAD)")
    serve_parser.add_argument("--host", default="127.0.0.1")
    serve_parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args(argv)
    root = args.root.resolve()

    if args.command == "validate":
        errors = validate(root)
        if errors:
            _print_errors(errors)
            return 1
        print(f"Validated {len(load_records(root)[0])} Atlas records.")
        return 0

    output = args.output if args.output.is_absolute() else root / args.output
    base_url = args.base_url
    if base_url is None:
        try:
            config = tomllib.loads((root / "atlas.toml").read_text(encoding="utf-8"))
            base_url = str(config.get("publication", {}).get("base_path", "/"))
        except (OSError, UnicodeError, tomllib.TOMLDecodeError):
            base_url = "/"
    errors = build_site(root, output, base_url, args.source_revision)
    if errors:
        _print_errors(errors)
        return 1
    print(f"Built Atlas at {output}.")
    if args.command == "serve":
        os.chdir(output)
        server = ThreadingHTTPServer((args.host, args.port), SimpleHTTPRequestHandler)
        print(f"Serving at http://{args.host}:{args.port}/")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
