import json
from html.parser import HTMLParser
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import atlas


class LinkInventory(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
        self.ids = set()

    def handle_starttag(self, tag, attributes):
        values = dict(attributes)
        if "href" in values:
            self.hrefs.append(values["href"])
        if "id" in values:
            self.ids.add(values["id"])


class AtlasValidationTests(unittest.TestCase):
    def record(self, identifier, kind="topic", **metadata):
        values = {
            "id": identifier,
            "kind": kind,
            "title": identifier.replace("-", " ").title(),
            "claim_status": "owner-directed",
        }
        values.update(metadata)
        return atlas.Record(Path(f"knowledge/{kind}s/{identifier}.md"), values, "Body")

    def test_rejects_duplicate_ids_and_dangling_relations(self):
        first = self.record("atlas")
        second = self.record("atlas")
        linked = self.record("model", relations=[{"type": "about", "target": "missing"}])

        errors = atlas.validate_records([first, second, linked])

        self.assertIn("duplicate-id", {error.code for error in errors})
        self.assertIn("missing-target", {error.code for error in errors})

    def test_rejects_parent_cycles(self):
        first = self.record("first", parent="second")
        second = self.record("second", parent="first")

        errors = atlas.validate_records([first, second])

        self.assertIn("parent-cycle", {error.code for error in errors})

    def test_does_not_invent_dates_for_undated_events(self):
        dated = self.record("dated", kind="event", date="2026-10-26")
        undated = self.record("undated", kind="event")

        self.assertEqual([dated], atlas.timeline_records([dated, undated]))

    def test_rejects_a_record_stored_under_the_wrong_kind(self):
        record = atlas.Record(
            Path("knowledge/questions/not-a-topic.md"),
            {"id": "not-a-topic", "kind": "topic", "title": "Wrong home", "claim_status": "owner-directed"},
            "Body",
        )

        errors = atlas.validate_records([record])

        self.assertIn("kind-path-mismatch", {error.code for error in errors})


class AtlasRenderingTests(unittest.TestCase):
    def test_markdown_html_is_escaped(self):
        rendered = atlas.render_markdown("<script>alert(1)</script>")

        self.assertNotIn("<script>", rendered)
        self.assertIn("&lt;script&gt;", rendered)

    def test_loads_toml_metadata_and_markdown_body(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            records = root / "knowledge/topics"
            records.mkdir(parents=True)
            (records / "atlas.md").write_text(
                '+++\nid = "atlas"\nkind = "topic"\ntitle = "Atlas"\n'
                'claim_status = "owner-directed"\n+++\n\nA map of knowledge.\n',
                encoding="utf-8",
            )

            loaded, errors = atlas.load_records(root)

        self.assertEqual([], errors)
        self.assertEqual("atlas", loaded[0].id)
        self.assertIn("A map of knowledge.", loaded[0].body)

    def test_build_writes_explainer_entrypoint_and_machine_export(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "site"
            root = Path(__file__).resolve().parents[1]

            source_revision = "b" * 40
            result = subprocess.run(
                [sys.executable, str(Path(__file__).resolve().parents[1] / "tools/atlas.py"),
                 "build", "--root", str(root), "--output", str(output), "--base-url", "/atlas/",
                 "--source-revision", source_revision],
                capture_output=True,
                text=True,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            home = (output / "index.html").read_text(encoding="utf-8")
            system = (output / "system.html").read_text(encoding="utf-8")
            search_page = (output / "search.html").read_text(encoding="utf-8")
            connections_page = (output / "connections.html").read_text(encoding="utf-8")
            timeline = (output / "timeline.html").read_text(encoding="utf-8")
            archive = (output / "archive.html").read_text(encoding="utf-8")
            data = (output / "atlas.json").read_text(encoding="utf-8")
            payload = json.loads(data)
            self.assertIn("A place to understand how the work fits together", home)
            self.assertIn("ONE RECORD SET · THREE PRIMARY VIEWS", home)
            self.assertIn("What Atlas is", home)
            self.assertIn("Review this bootstrap", home)
            self.assertIn("Broader Vapor and Loo-Cast knowledge will wait", home)
            self.assertIn('href="/atlas/records/entrypoint-review.html"', home)
            self.assertIn('class="system-link"', home)
            self.assertIn("How Atlas works", system)
            self.assertIn("SYSTEM REFERENCE", system)
            self.assertIn("Authored data and generation", system)
            self.assertIn("disposable bootstrap visualization", system)
            self.assertIn("Follow the generated views", system)
            self.assertIn("/atlas/timeline.html", home)
            self.assertIn("Search Atlas", search_page)
            self.assertIn('role="tablist"', search_page)
            self.assertIn('data-kind="question"', search_page)
            self.assertIn(">Questions</button>", search_page)
            search_header = search_page.split("<main>", 1)[0]
            self.assertIn('href="/atlas/search.html" aria-current="page">Search</a>', search_header)
            self.assertNotIn("Questions", search_header)
            self.assertNotIn("structure.html", search_page)
            self.assertIn('id="connection-record"', connections_page)
            self.assertIn('id="connection-type"', connections_page)
            self.assertIn('id="connection-direction"', connections_page)
            self.assertIn("direction authored", connections_page)
            self.assertIn("clarifies", connections_page)
            self.assertIn("entrypoint-review", connections_page)
            self.assertIn('href="/atlas/connections.html" aria-current="page">Connections</a>', connections_page.split("<main>", 1)[0])
            self.assertIn('href="/atlas/records/entrypoint-review.html"', connections_page)
            self.assertIn('href="/atlas/connections.html?record=entrypoint-review"', connections_page)
            self.assertTrue((output / "assets" / "connections.js").is_file())
            self.assertFalse((output / "structure.html").exists())
            self.assertIn("Record types", system)
            self.assertIn("not independently confirmed", system)
            self.assertIn("Atlas bootstrap and audit preservation", timeline)
            self.assertIn('"id": "atlas"', data)
            self.assertEqual(1, payload["schema_version"])
            self.assertEqual("/atlas/", payload["publication"]["base_path"])
            self.assertEqual("https://vapor.ghf-studios.site/atlas/", payload["publication"]["public_url"])
            self.assertEqual(source_revision, payload["source_revision"])
            self.assertIn(
                {"id": "audit-snapshot", "kind": "evidence", "claim_status": "historical-snapshot"},
                payload["graph"]["nodes"],
            )
            self.assertIn(
                {"source": "atlas-bootstrap", "type": "preserves", "target": "audit-snapshot"},
                payload["graph"]["edges"],
            )
            self.assertIn('id="atlas-search"', search_page)
            self.assertNotIn('id="atlas-search"', home)
            self.assertNotIn('id="atlas-search"', timeline)
            self.assertIn("Preserved audit material", home)
            archive_page = output / "archive/read/README.md.html"
            self.assertTrue(archive_page.is_file())
            self.assertTrue((output / "archive/audit-snapshot-2026-10-26/README.md").is_file())
            self.assertIn("/atlas/archive/read/README.md.html", archive)
            self.assertIn("/atlas/archive/audit-snapshot-2026-10-26/README.md", archive)
            readme_page = archive_page.read_text(encoding="utf-8")
            self.assertIn("Loo-Cast / Vapor cross-product audit", readme_page)
            self.assertIn(f"/blob/{source_revision}/archive/audit-snapshot-2026-10-26/README.md", readme_page)
            self.assertIn("Download original", archive_page.read_text(encoding="utf-8"))
            self.assertIn(f"/tree/{source_revision}/archive/audit-snapshot-2026-10-26", archive)
            evidence_page = (output / "archive/read/vapor-ecosystem-evidence-atlas.md.html").read_text(encoding="utf-8")
            self.assertNotIn('href="/home/leslieghf/', evidence_page)
            self.assertIn("Search", home.split("</nav>", 1)[0])
            self.assertIn("Connections", home.split("</nav>", 1)[0])
            self.assertIn("Timeline", home.split("</nav>", 1)[0])
            self.assertIn('class="system-link"', home)
            self.assertNotIn("archive.html", home.split("</nav>", 1)[0])
            self.assertIn("Questions are one record type", search_page)
            self.assertIn("not a timeline dataset", timeline)
            self.assertNotIn("/archive/audit-snapshot-2026-10-26/loo-cast-vapor-history-timeline.md", timeline)
            self.assertIn(
                {"source": "atlas-bootstrap-workstream", "type": "parent", "target": "atlas"},
                payload["graph"]["edges"],
            )
            self.assertIn('href="/atlas/connections.html"', (output / "records" / "atlas-system.html").read_text(encoding="utf-8"))
            self.assertTrue((output / "records" / "claim-basis-and-review-state.html").is_file())
            self.assertTrue((output / "records" / "relation-vocabulary.html").is_file())
            self.assertTrue((output / "records" / "time-and-validity.html").is_file())
            self.assertTrue((output / "records" / "source-identity.html").is_file())
            atlas_page = (output / "records/atlas.html").read_text(encoding="utf-8")
            self.assertIn("contains", atlas_page)
            self.assertIn("atlas-system", atlas_page)
            self.assertIn(f"/blob/{source_revision}/knowledge/topics/atlas.md", atlas_page)
            self.assertNotIn("/blob/main/knowledge/topics/atlas.md", atlas_page)
            self.assertFalse((output / "about-atlas.html").exists())
            self.assertFalse((output / "map.html").exists())
            self.assertFalse((output / "questions.html").exists())
            for page in ("product", "authoring", "site", "generator", "search-and-export", "validation", "publishing", "scope"):
                self.assertTrue((output / "records" / f"atlas-{page}.html").is_file(), page)
            self.assertIn("not a server", (output / "records/atlas-scope.html").read_text(encoding="utf-8"))

            documents = {}
            for html_path in output.rglob("*.html"):
                parser = LinkInventory()
                parser.feed(html_path.read_text(encoding="utf-8"))
                documents[html_path] = parser
            for html_path, parser in documents.items():
                for href in parser.hrefs:
                    target = urlsplit(href)
                    if target.scheme or target.netloc:
                        continue
                    path = unquote(target.path)
                    if path.startswith("/atlas/"):
                        relative = path.removeprefix("/atlas/")
                    elif path.startswith("/"):
                        continue
                    else:
                        relative = path
                    linked_page = (output / relative) if relative else html_path
                    if linked_page.is_dir():
                        linked_page /= "index.html"
                    self.assertTrue(linked_page.is_file(), f"{html_path.relative_to(output)} links to missing {href}")
                    # Historical Markdown is preserved verbatim and may contain
                    # already-dangling fragments; Atlas verifies its local file
                    # routes without claiming to repair those source references.
                    source_is_archived_reference = html_path.relative_to(output).as_posix().startswith("archive/read/")
                    if target.fragment and not source_is_archived_reference:
                        destination = documents.get(linked_page)
                        if destination is not None:
                            self.assertIn(unquote(target.fragment), destination.ids, f"{href} has no matching anchor")

            default_output = Path(temporary) / "default-base-site"
            default_build = subprocess.run(
                [sys.executable, str(Path(__file__).resolve().parents[1] / "tools/atlas.py"),
                 "build", "--root", str(root), "--output", str(default_output)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, default_build.returncode, default_build.stderr)
            self.assertIn('/search.html', (default_output / "index.html").read_text(encoding="utf-8"))
            self.assertIn('/connections.html', (default_output / "index.html").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
