#!/usr/bin/env python3
"""Validate Atlas records and build a dependency-free static site."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date, datetime
from html import escape
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import sys
import tomllib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from typing import Any


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


def _inline_markdown(text: str) -> str:
    escaped = escape(text, quote=True)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", escaped)

    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

    def link(match: re.Match[str]) -> str:
        label = match.group(1)
        target = match.group(2)
        decoded_target = target.replace("&amp;", "&")
        if decoded_target.startswith(("https://", "http://", "mailto:", "/", "#")):
            return f'<a href="{target}">{label}</a>'
        return label

    return link_pattern.sub(link, escaped)


def render_markdown(markdown: str) -> str:
    """Render a conservative Markdown subset; raw HTML is always escaped."""
    output: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []
    code_lines: list[str] | None = None

    def flush_paragraph() -> None:
        if paragraph:
            output.append("<p>" + _inline_markdown(" ".join(part.strip() for part in paragraph)) + "</p>")
            paragraph.clear()

    def flush_list() -> None:
        if list_items:
            output.append("<ul>" + "".join(f"<li>{_inline_markdown(item)}</li>" for item in list_items) + "</ul>")
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
            output.append(f"<h{level}>{_inline_markdown(heading.group(2))}</h{level}>")
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
    links = [("Home", "index.html"), ("System", "system.html"), ("Map", "map.html"), ("Timeline", "timeline.html"), ("Questions", "questions.html"), ("Archive", "archive.html")]
    nav = "".join(
        f'<a href="{base}{route}"{(" aria-current=\"page\"" if active == route else "")}>{label}</a>'
        for label, route in links
    )
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
</head>
<body>
  <header class="site-header"><a class="brand" href="{base}index.html"><span class="brand-mark">A</span><span>Atlas<small>GHF Studios product · knowledge system</small></span></a><nav aria-label="Main navigation">{nav}</nav></header>
  <main>{content}</main>
  <footer><span>Atlas is generated from versioned Markdown records.</span><span><a href="{base}atlas.json">Structured data</a> · <a href="https://github.com/GHF-Studios/Atlas">Source repository</a></span></footer>
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


def _source_url(path: str) -> str:
    return "https://github.com/GHF-Studios/Atlas/blob/main/" + "/".join(escape(part, quote=True) for part in PurePosixPath(path).parts)


def build_site(root: Path, output: Path, base_url: str = "/") -> list[ValidationError]:
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
    by_id = {record.id: record for record in records}
    output.mkdir(parents=True, exist_ok=True)
    (output / "assets").mkdir(exist_ok=True)
    (output / "records").mkdir(exist_ok=True)
    shutil.copyfile(root / "site/assets/style.css", output / "assets/style.css")
    shutil.copyfile(root / "site/assets/search.js", output / "assets/search.js")

    # A typed and queryable export; chronology is a projection over dated events.
    payload = {
        "schema_version": 1,
        "atlas": _toml_scalar(config.get("atlas", {})),
        "publication": _toml_scalar(config.get("publication", {})),
        "graph": _graph_json(records),
        "records": [_record_json(record, root) for record in sorted(records, key=lambda item: (item.kind, item.title.casefold(), item.id))],
    }
    (output / "atlas.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    search = '''<section class="search-box" aria-label="Search Atlas"><label for="atlas-search">Search Atlas</label><input id="atlas-search" type="search" placeholder="Search questions, decisions, evidence…" autocomplete="off"><div id="atlas-search-results" aria-live="polite"></div></section>'''

    home_record_ids = ("atlas-product", "knowledge-model", "atlas-scope")
    home_records = [by_id[key] for key in home_record_ids if key in by_id]
    home = f'''<section class="hero"><p class="eyebrow">GHF STUDIOS · PRODUCT 03</p><h1>Atlas makes the work understandable.</h1><p class="lead">Atlas is a product in its own right: a versioned knowledge system, with a navigable website generated from its records. This first knowledge set describes Atlas itself.</p><p class="actions"><a class="button primary" href="{base}records/atlas-product.html">Understand Atlas</a><a class="button" href="{base}map.html">Explore its knowledge map</a><a class="button" href="{base}timeline.html">Browse dated events</a></p></section>
<section class="intro-grid"><article class="panel"><h2>One product among three</h2><p>GHF Studios’ current product picture names Vapor, Loo-Cast, and Atlas as distinct products. Atlas is the product being explained here; it does not absorb or stand in for the others.</p><p><a href="{base}records/atlas-product.html">Product role and boundaries →</a></p></article><article class="panel"><h2>How Atlas works</h2><p>People author typed Markdown records in Git. A small generator validates them and builds the website and machine-readable graph export. The website is a view; the repository is the source.</p><p><a href="{base}records/atlas-authoring.html">Authoring model →</a> · <a href="{base}records/atlas-generator.html">Build path →</a></p></article><article class="panel"><h2>What this proves</h2><p>The first dataset is intentionally Atlas itself: product intent, knowledge structure, site, generation, search, validation, deployment, and known limits. This is a bootstrap, not a claim that the wider knowledge base is complete.</p><p><a href="{base}records/atlas-scope.html">Current scope and absences →</a></p></article></section>
<section class="section"><div class="section-heading"><div><p class="eyebrow">ATLAS, EXPLAINED BY ATLAS</p><h2>Start with these</h2></div><a href="{base}system.html">How Atlas is built →</a></div><div class="cards">{''.join(_record_card(record, base) for record in home_records)}</div></section>
<section class="section"><div class="section-heading"><div><p class="eyebrow">OPEN FOR REVIEW</p><h2>Questions that shape the next iteration</h2></div><a href="{base}questions.html">All questions →</a></div><div class="cards">{_record_card(by_id['entrypoint-review'], base) if 'entrypoint-review' in by_id else '<p>No review question is recorded yet.</p>'}</div></section>
<section class="section"><h2>Find a record</h2>{search}</section>
<aside class="notice"><strong>Honest boundary.</strong> The product relationships and intended role are owner direction. Technical descriptions marked source-verified describe the current Atlas repository. Atlas is not yet a complete organizational history, discussion platform, or automated mirror of other products.</aside>'''
    (output / "index.html").write_text(_page("Home", home, base, "index.html"), encoding="utf-8")

    system_sections = [
        ("Product and model", ("atlas-product", "knowledge-model", "timeline-is-a-view", "current-site-is-disposable-bootstrap")),
        ("Authored data and generation", ("atlas-authoring", "atlas-generator", "atlas-validation")),
        ("Published experience", ("atlas-site", "atlas-search-and-export", "atlas-publishing")),
        ("Boundaries and open design", ("atlas-scope", "entrypoint-review")),
    ]
    system_html = '<section class="page-intro"><p class="eyebrow">ATLAS, EXPLAINED BY ATLAS</p><h1>How Atlas is built</h1><p>This guide describes Atlas as a product and the current implementation behind it. Product intent is labeled as owner direction; implementation claims link to the files that establish them. Each card opens the full record.</p></section>'
    for heading, identifiers in system_sections:
        section_records = [by_id[identifier] for identifier in identifiers if identifier in by_id]
        if section_records:
            system_html += f'<section class="section"><h2>{escape(heading)}</h2><div class="cards">{"".join(_record_card(record, base) for record in section_records)}</div></section>'
    (output / "system.html").write_text(_page("How Atlas is built", system_html, base, "system.html"), encoding="utf-8")

    groups: list[str] = []
    for kind in KIND_DIRS:
        members = [record for record in records if record.kind == kind]
        if not members:
            continue
        cards = "".join(_record_card(record, base) for record in sorted(members, key=lambda item: item.title.casefold()))
        groups.append(f'<section class="section"><h2>{escape(kind.replace("-", " ").title())} <small>{len(members)}</small></h2><div class="cards">{cards}</div></section>')
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
    guide = f'''<section class="section guide-grid" id="record-types"><article class="panel"><h2>Record types <small>bootstrap vocabulary</small></h2><table><tbody>{kind_rows}</tbody></table></article><article class="panel"><h2>Claim status <small>what confidence means</small></h2><table><tbody>{status_rows}</tbody></table></article></section>'''
    map_body = '<section class="page-intro"><p class="eyebrow">STRUCTURE</p><h1>Knowledge map</h1><p>Each record has one primary kind and may connect to other records. Parent links show the main hierarchy; typed relations make cross-links explicit. The vocabulary and definitions below are the current bootstrap draft.</p></section>' + guide + "".join(groups)
    (output / "map.html").write_text(_page("Knowledge map", map_body, base, "map.html"), encoding="utf-8")

    events = timeline_records(records)
    if events:
        timeline_body = '<section class="page-intro"><p class="eyebrow">DATED EVENTS</p><h1>Timeline</h1><p>This view contains only events with dates. It is generated from event records and remains independent of the knowledge map.</p></section><ol class="timeline">'
        timeline_body += "".join(f'<li><time datetime="{escape(str(_toml_scalar(event.metadata["date"])), quote=True)}">{escape(str(_toml_scalar(event.metadata["date"])))}</time>{_record_card(event, base)}</li>' for event in events)
        timeline_body += "</ol>"
    else:
        timeline_body = '<section class="page-intro"><p class="eyebrow">DATED EVENTS</p><h1>Timeline</h1></section><div class="empty-state"><h2>No dated events</h2><p>Undated knowledge stays on the map. Atlas does not invent dates to fill this view.</p></div>'
    timeline_body += f'<section class="section"><h2>Historical timeline source</h2><p>The archived audit contains a much deeper historical reconstruction; it remains an unreviewed source document rather than imported timeline records.</p><p><a href="{_source_url("archive/audit-snapshot-2026-10-26/loo-cast-vapor-history-timeline.md")}">Read the preserved history report</a> · <a href="{_source_url("archive/audit-snapshot-2026-10-26/loo-cast-vapor-mega-timeline.svg")}">Open the rendered timeline diagram</a></p></section>'
    (output / "timeline.html").write_text(_page("Timeline", timeline_body, base, "timeline.html"), encoding="utf-8")

    questions = [record for record in records if record.kind == "question"]
    question_body = '<section class="page-intro"><p class="eyebrow">OPEN QUESTIONS</p><h1>Questions</h1><p>Questions are first-class records. They remain open until a decision or new evidence resolves them.</p></section>'
    question_body += '<div class="cards">' + ("".join(_record_card(record, base) for record in questions) or '<div class="empty-state"><p>No questions are recorded.</p></div>') + '</div>'
    (output / "questions.html").write_text(_page("Questions", question_body, base, "questions.html"), encoding="utf-8")

    archive_dir = root / "archive/audit-snapshot-2026-10-26"
    archive_items = sorted(path for path in archive_dir.rglob("*") if path.is_file() and path.name != "PRESERVATION.md")
    archive_links = "".join(
        f'<li><a href="{_source_url(_relative_path(path, root))}">{escape(_relative_path(path, root).removeprefix("archive/audit-snapshot-2026-10-26/"))}</a></li>'
        for path in archive_items
    )
    archive_body = f'''<section class="page-intro"><p class="eyebrow">HISTORICAL WORKING MATERIAL</p><h1>Preserved audit bundle</h1><p>This is the earlier Loo-Cast/Vapor audit and timeline work, preserved before Atlas implementation. It is not an approved knowledge model, a complete audit, or a statement that every historical claim is current.</p><p><a class="button" href="{_source_url("archive/audit-snapshot-2026-10-26/README.md")}">Read the bundle guide</a> <a class="button" href="{_source_url("archive/audit-snapshot-2026-10-26/PRESERVATION.md")}">File-by-file preservation manifest</a></p></section><section class="section"><h2>Browse files <small>{len(archive_items)}</small></h2><ul class="file-list">{archive_links}</ul></section>'''
    (output / "archive.html").write_text(_page("Preserved audit", archive_body, base, "archive.html"), encoding="utf-8")

    for record in records:
        details = [f'<span class="badge">{escape(record.kind)}</span>', f'<span class="badge status">{escape(record.claim_status)}</span>']
        if record.metadata.get("date") is not None:
            details.append(f'<time class="badge" datetime="{escape(str(_toml_scalar(record.metadata["date"])), quote=True)}">{escape(str(_toml_scalar(record.metadata["date"])))}</time>')
        parent_id = record.metadata.get("parent")
        parent = f'<p><strong>Parent:</strong> {_record_link(by_id[parent_id], base)}</p>' if parent_id in by_id else ""
        relations = record.metadata.get("relations", [])
        relation_html = "".join(f'<li><span class="relation">{escape(rel["type"])}</span> → {_record_link(by_id[rel["target"]], base)}</li>' for rel in relations)
        source_html = "".join(f'<li><a href="{_source_url(source)}">{escape(source)}</a></li>' for source in record.metadata.get("sources", []))
        record_body = f'''<section class="page-intro"><p class="eyebrow">RECORD · {escape(record.id)}</p><h1>{escape(record.title)}</h1><div class="badges">{"".join(details)}</div></section><article class="record-body">{render_markdown(record.body)}</article><section class="section"><h2>Connections</h2>{parent}<ul>{relation_html or '<li>No typed cross-links.</li>'}</ul></section><section class="section"><h2>Sources</h2><ul>{source_html or '<li>No source path listed.</li>'}</ul><p class="source-path">Authored at <a href="{_source_url(_relative_path(record.path, root))}">{escape(_relative_path(record.path, root))}</a></p></section>'''
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
    serve_parser = subparsers.add_parser("serve", help="build and serve Atlas locally")
    serve_parser.add_argument("--root", type=Path, default=Path.cwd())
    serve_parser.add_argument("--output", type=Path, default=Path("dist"))
    serve_parser.add_argument("--base-url", default="/")
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
    errors = build_site(root, output, base_url)
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
