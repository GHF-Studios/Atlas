import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import atlas


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

            result = subprocess.run(
                [sys.executable, str(Path(__file__).resolve().parents[1] / "tools/atlas.py"),
                 "build", "--root", str(root), "--output", str(output), "--base-url", "/Atlas/"],
                capture_output=True,
                text=True,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            home = (output / "index.html").read_text(encoding="utf-8")
            map_page = (output / "map.html").read_text(encoding="utf-8")
            timeline = (output / "timeline.html").read_text(encoding="utf-8")
            data = (output / "atlas.json").read_text(encoding="utf-8")
            payload = json.loads(data)
            self.assertIn("What Atlas is", home)
            self.assertIn("/Atlas/timeline.html", home)
            self.assertIn("Record types", map_page)
            self.assertIn("not independently confirmed", map_page)
            self.assertIn("Atlas bootstrap and audit preservation", timeline)
            self.assertIn('"id": "atlas"', data)
            self.assertEqual(1, payload["schema_version"])
            self.assertIn(
                {"id": "audit-snapshot", "kind": "evidence", "claim_status": "historical-snapshot"},
                payload["graph"]["nodes"],
            )
            self.assertIn(
                {"source": "atlas-bootstrap", "type": "preserves", "target": "audit-snapshot"},
                payload["graph"]["edges"],
            )
            self.assertIn('/Atlas/atlas.json', home)
            self.assertIn(
                {"source": "atlas-bootstrap-workstream", "type": "parent", "target": "atlas"},
                payload["graph"]["edges"],
            )


if __name__ == "__main__":
    unittest.main()
