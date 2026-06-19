import argparse
import contextlib
import importlib.util
import io
import shutil
import unittest
import uuid
from pathlib import Path


ENGINE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "codex_council_v2.py"
spec = importlib.util.spec_from_file_location("codex_council_v2_engine", ENGINE_PATH)
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)


class EngineTest(unittest.TestCase):
    def setUp(self):
        self.tmp_path = engine.ROOT / "_test-tmp" / uuid.uuid4().hex
        self.tmp_path.mkdir(parents=True, exist_ok=True)
        self.old_runs = engine.RUNS
        engine.RUNS = self.tmp_path / "runs"

    def tearDown(self):
        engine.RUNS = self.old_runs
        if self.tmp_path.exists():
            shutil.rmtree(self.tmp_path, ignore_errors=True)

    def init(self, run_id="unit-run"):
        return engine.init_run(argparse.Namespace(run_id=run_id, title="Unit", question="Unit question?", force=True))

    def approve_and_open(self, run_dir):
        engine.validate_charter(argparse.Namespace(run_dir=str(run_dir)))
        engine.open_evidence_requests(argparse.Namespace(run_dir=str(run_dir)))

    def add_evidence(self, run_dir):
        req = engine.register_evidence_request_record(run_dir, "executor", "What is the fixture support budget?", "support", "SYNTHETIC", 9999, "INTERNAL_PROJECT_FACT")
        ev = engine.resolve_evidence_request_record(run_dir, req["request_id"], "Fixture support budget is 20 hours/month, not 200.", "INTERNAL_PROJECT_FACT", "Fixture Cost Sheet")
        engine.mark_evidence_ready(argparse.Namespace(run_dir=str(run_dir)))
        return ev

    def submit_all_memos(self, run_dir, bad_expansionist=True):
        for executive in engine.EXECUTIVES:
            economic = "The fixture has 200 support hours/month." if executive == "expansionist" and bad_expansionist else "The fixture support budget is 20 hours/month."
            content = engine.memo_text("unit-run", executive, f"{executive} position.", "Role-specific reasoning.", economic, ["EV-0001"])
            engine.submit_memo_record(run_dir, executive, content)

    def test_event_tag_validation_rejects_bad_id(self):
        failures = engine.validate_event_tags("[FACT_CHECK:BAD-1]", "memo")
        self.assertTrue(failures)

    def test_cache_deduplicates_equivalent_request(self):
        run_dir = self.init()
        self.approve_and_open(run_dir)
        first = engine.register_evidence_request_record(run_dir, "contrarian", "What is the fixture demand cap?", "pilot", "SYNTHETIC", 9999, "SCENARIO_ASSUMPTION")
        engine.resolve_evidence_request_record(run_dir, first["request_id"], "Fixture demand is capped at 40 orders/day.", "SCENARIO_ASSUMPTION", "Fixture Note")
        second = engine.register_evidence_request_record(run_dir, "outsider", "What is the fixture demand cap?", "pilot", "SYNTHETIC", 9999, "SCENARIO_ASSUMPTION")
        self.assertEqual(second["status"], "ANSWERED_FROM_CACHE")
        self.assertEqual(second["answer_source"], "cache")

    def test_illegal_stage_transition_rejected(self):
        run_dir = self.init()
        with self.assertRaises(SystemExit):
            engine.transition(run_dir, "EVIDENCE_READY", "skip charter")

    def test_blocking_fact_check_requires_current_memo_correction(self):
        run_dir = self.init()
        self.approve_and_open(run_dir)
        ev = self.add_evidence(run_dir)
        self.submit_all_memos(run_dir, bad_expansionist=True)
        engine.transition(run_dir, "AUDIT_IN_PROGRESS", "unit audit")
        claims = engine.extract_claims_record(run_dir)
        bad = next(c for c in claims if "200 support hours" in c["exact_text"])
        engine.record_fact_check_record(run_dir, bad["claim_id"], "False", "Replace 200 with 20.", [ev["evidence_id"]], "RESOLVED", "The fixture has 200 support hours/month.", "The fixture support budget is 20 hours/month.")
        failures = engine.validate_audit_record(run_dir)
        self.assertTrue(any("contradicted claim remains" in failure for failure in failures))

    def test_veto_scope_validation_demotes_invalid_domain(self):
        run_dir = self.init()
        self.approve_and_open(run_dir)
        self.add_evidence(run_dir)
        self.submit_all_memos(run_dir, bad_expansionist=False)
        valid = engine.record_veto_record(run_dir, "executor", "PRE_CHAIR", "feasible next action", "executor position.", "No owner.", "EV-0001", "Assign owner.")
        invalid = engine.record_veto_record(run_dir, "outsider", "PRE_CHAIR", "brand preference", "outsider position.", "Naming.", "none", "Rename.")
        self.assertTrue(valid["valid"])
        self.assertFalse(invalid["valid"])
        self.assertEqual(invalid["status"], "DEMOTED_TO_OBJECTION")

    def test_final_verdict_surfaces_unresolved_valid_vetoes_only(self):
        run_dir = self.init()
        engine.write(run_dir / "CHAIRMAN.md", "# Chairman File\n\n## Provisional Verdict\nStart without owner assignment.\n")
        valid_judgment = engine.record_veto_record(
            run_dir,
            "executor",
            "POST_CHAIR",
            "feasible next action",
            "Start without owner assignment.",
            "Needs judgment.",
            "RUN_CHARTER",
            "Chairman must decide.",
            challenged_artifact="CHAIRMAN.md",
            verification_method="requires_judgment",
        )
        resolved = engine.record_veto_record(
            run_dir,
            "executor",
            "POST_CHAIR",
            "feasible next action",
            "Start without owner assignment.",
            "Needs owner.",
            "RUN_CHARTER",
            "Owner: Fixture Lead",
            challenged_artifact="CHAIRMAN.md",
            remedy_must_contain="Owner: Fixture Lead",
        )
        engine.append(run_dir / "CHAIRMAN.md", "\nOwner: Fixture Lead\n")
        engine.resolve_veto_record(run_dir, resolved["veto_id"])
        invalid = engine.record_veto_record(run_dir, "outsider", "POST_CHAIR", "brand preference", "Start without owner assignment.", "Naming.", "none", "Rename.")
        data = engine.status(run_dir)
        data["stage"] = "POST_CHAIR_VETO_REVIEW"
        data["last_valid_stage"] = "POST_CHAIR_VETO_REVIEW"
        engine.save_json(engine.status_path(run_dir), data)
        engine.record_final_verdict(argparse.Namespace(run_dir=str(run_dir), text="Final text.", summary="summary", next_action="next"))
        chairman = engine.read(run_dir / "CHAIRMAN.md")
        unresolved_section = chairman.split("Unresolved valid vetoes surfaced to human owner:")[-1].split("Out-of-scope veto attempts")[0]
        self.assertIn(valid_judgment["veto_id"], unresolved_section)
        self.assertNotIn(resolved["veto_id"], unresolved_section)
        self.assertIn(invalid["veto_id"], chairman)
        self.assertIn("ordinary dissent", chairman)

    def test_veto_remedy_must_be_verified(self):
        run_dir = self.init()
        self.approve_and_open(run_dir)
        self.add_evidence(run_dir)
        self.submit_all_memos(run_dir, bad_expansionist=False)
        veto = engine.record_veto_record(
            run_dir,
            "executor",
            "PRE_CHAIR",
            "feasible next action",
            "executor position.",
            "No owner.",
            "EV-0001",
            "Assign owner.",
            challenged_artifact="memos/executor.md",
            challenged_section="CURRENT_MEMO",
            remedy_must_contain="Owner: Fixture Lead",
        )
        vetoes = engine.load_json(run_dir / "VETOES.json", [])
        vetoes[0]["status"] = "RESOLVED"
        engine.save_json(run_dir / "VETOES.json", vetoes)
        with self.assertRaises(SystemExit):
            engine.validate_run(argparse.Namespace(run_dir=str(run_dir)))
        content = engine.read(run_dir / "memos" / "executor.md").replace("Role-specific reasoning.", "Role-specific reasoning. Unrelated text.")
        engine.write(run_dir / "memos" / "executor.md", content)
        with self.assertRaises(SystemExit):
            engine.resolve_veto_record(run_dir, veto["veto_id"])
        content = engine.read(run_dir / "memos" / "executor.md").replace("Unrelated text.", "Owner: Fixture Lead.")
        engine.write(run_dir / "memos" / "executor.md", content)
        resolved = engine.resolve_veto_record(run_dir, veto["veto_id"])
        self.assertEqual(resolved["status"], "RESOLVED")

    def test_anonymous_packets_do_not_leak_source_key(self):
        run_dir = self.init()
        self.approve_and_open(run_dir)
        self.add_evidence(run_dir)
        self.submit_all_memos(run_dir, bad_expansionist=False)
        engine.transition(run_dir, "AUDIT_IN_PROGRESS", "unit audit")
        self.assertFalse(engine.validate_audit_record(run_dir))
        engine.create_anonymous_review_packets(argparse.Namespace(run_dir=str(run_dir)))
        route = engine.load_json(run_dir / "_work" / "review-routing-map.private.json", [])[0]
        packet = engine.read(engine.stored_path(run_dir, route["packet_path"]))
        self.assertNotIn(route["source_memo"], packet)

    def test_stored_paths_accept_posix_and_windows_separators(self):
        run_dir = self.init()
        self.approve_and_open(run_dir)
        self.add_evidence(run_dir)
        self.submit_all_memos(run_dir, bad_expansionist=False)
        engine.transition(run_dir, "AUDIT_IN_PROGRESS", "unit audit")
        self.assertFalse(engine.validate_audit_record(run_dir))
        engine.create_anonymous_review_packets(argparse.Namespace(run_dir=str(run_dir)))
        route = engine.load_json(run_dir / "_work" / "review-routing-map.private.json", [])[0]
        self.assertIn("/", route["packet_path"])
        self.assertTrue(engine.stored_path(run_dir, route["packet_path"]).exists())
        self.assertTrue(engine.stored_path(run_dir, route["packet_path"].replace("/", "\\")).exists())

    def test_review_completeness_requires_all_twenty_or_waiver(self):
        run_dir = self.init()
        self.approve_and_open(run_dir)
        self.add_evidence(run_dir)
        self.submit_all_memos(run_dir, bad_expansionist=False)
        engine.transition(run_dir, "AUDIT_IN_PROGRESS", "unit audit")
        self.assertFalse(engine.validate_audit_record(run_dir))
        engine.create_anonymous_review_packets(argparse.Namespace(run_dir=str(run_dir)))
        route_map = engine.load_json(run_dir / "_work" / "review-routing-map.private.json", [])
        self.assertEqual(len(route_map), 20)
        for route in route_map[:19]:
            engine.record_peer_review_record(run_dir, route["packet_id"], "Review submitted.")
        with self.assertRaises(SystemExit):
            engine.merge_review_events(argparse.Namespace(run_dir=str(run_dir)))
        engine.waive_peer_review_record(run_dir, route_map[19]["assignment_id"], "Reviewer unavailable after retry.")
        engine.merge_review_events(argparse.Namespace(run_dir=str(run_dir)))
        engine.prepare_chairman_packet(argparse.Namespace(run_dir=str(run_dir), allow_open_vetoes=True))
        packet = engine.read(run_dir / "_work" / "CHAIRMAN_PACKET.md")
        self.assertIn("Reviewer unavailable after retry.", packet)

    def test_review_completeness_all_twenty_can_advance(self):
        run_dir = self.init("unit-run-20")
        self.approve_and_open(run_dir)
        self.add_evidence(run_dir)
        self.submit_all_memos(run_dir, bad_expansionist=False)
        engine.transition(run_dir, "AUDIT_IN_PROGRESS", "unit audit")
        self.assertFalse(engine.validate_audit_record(run_dir))
        engine.create_anonymous_review_packets(argparse.Namespace(run_dir=str(run_dir)))
        for route in engine.load_json(run_dir / "_work" / "review-routing-map.private.json", []):
            engine.record_peer_review_record(run_dir, route["packet_id"], "Review submitted.")
        engine.merge_review_events(argparse.Namespace(run_dir=str(run_dir)))
        self.assertEqual(engine.status(run_dir)["stage"], "AUTHOR_REVISION")

    def test_expanded_claim_extraction_detects_commercial_claims(self):
        text = "The setup fee is AED 499. Margin with revenue AED 100 and cost AED 60 is 70%. AED 100 per month equals AED 1,000 annually. This is guaranteed to be best. Scenario assumption: conversion is 5%."
        claim_types = []
        notes = []
        classifications = []
        for sentence in engine.split_claim_sentences(text):
            types, values = engine.detect_claim_values(sentence)
            claim_types.extend(types)
            notes.extend(engine.deterministic_audit_notes(sentence, values))
            classifications.append(engine.claim_classification(sentence))
        self.assertIn("MONEY", claim_types)
        self.assertIn("PERCENTAGE_OR_RATIO", claim_types)
        self.assertIn("DATE_OR_PERIOD", claim_types)
        self.assertIn("ABSOLUTE_LANGUAGE", claim_types)
        self.assertTrue(any("BROKEN_MARGIN" in note for note in notes))
        self.assertTrue(any("BROKEN_MONTHLY_TO_ANNUAL" in note for note in notes))
        self.assertIn("SCENARIO_ASSUMPTION", classifications)

    def test_resume_reports_next_action_after_interruption(self):
        run_dir = self.init()
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            engine.resume(argparse.Namespace(run_dir=str(run_dir)))
        output = buf.getvalue()
        self.assertIn("validate-charter", output)
        self.assertIn("expected_next_agent", output)
        self.assertIn("required_input_files", output)

    def test_resume_interruptions_do_not_duplicate_completed_work(self):
        run_dir = self.init()
        self.approve_and_open(run_dir)
        first = engine.register_evidence_request_record(run_dir, "contrarian", "What is the fixture demand cap?", "pilot", "SYNTHETIC", 9999, "SCENARIO_ASSUMPTION")
        engine.resolve_evidence_request_record(run_dir, first["request_id"], "Fixture demand is capped at 40 orders/day.", "SCENARIO_ASSUMPTION", "Fixture Note")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            engine.resume(argparse.Namespace(run_dir=str(run_dir)))
        self.assertIn("mark-evidence-ready", buf.getvalue())
        requests_before = len(engine.load_json(run_dir / "evidence" / "EVIDENCE_LIBRARY.json", {}).get("requests", []))
        with contextlib.redirect_stdout(io.StringIO()):
            engine.resume(argparse.Namespace(run_dir=str(run_dir)))
        requests_after = len(engine.load_json(run_dir / "evidence" / "EVIDENCE_LIBRARY.json", {}).get("requests", []))
        self.assertEqual(requests_before, requests_after)

    def test_file_lock_prevents_double_lock(self):
        run_dir = self.init()
        with engine.file_lock(run_dir, "unit"):
            with self.assertRaises(SystemExit):
                with engine.file_lock(run_dir, "unit"):
                    pass

    def test_full_synthetic_pipeline_and_old_hash_manifest(self):
        run_dir = engine.synthetic_test(argparse.Namespace())
        expansionist = engine.current_memo(engine.read(run_dir / "memos" / "expansionist.md"))
        self.assertNotIn("The fixture has 200 support hours/month.", expansionist)
        self.assertIn("The fixture support budget is 20 hours/month.", expansionist)
        before = engine.load_json(run_dir / "_work" / "old-system-hashes-before.json", {})
        after = engine.load_json(run_dir / "_work" / "old-system-hashes-after.json", {})
        self.assertEqual(before, after)
        vetoes = engine.load_json(run_dir / "VETOES.json", [])
        pre = next(v for v in vetoes if v["veto_id"] == "V-0001")
        self.assertTrue(pre["valid"])
        self.assertEqual(pre["status"], "RESOLVED")
        self.assertEqual(pre["validation_reason"], "required remedy text found")

    def test_release_tree_rejects_test_tmp_and_requires_entry_points(self):
        package_root = self.tmp_path / "package"
        (package_root / "_test-tmp").mkdir(parents=True)
        failures = engine.release_tree_failures(package_root)
        self.assertTrue(any("_test-tmp" in failure for failure in failures))
        self.assertTrue(any("Missing .agents/skills/codex-council-v2/SKILL.md" in failure for failure in failures))


if __name__ == "__main__":
    unittest.main()
