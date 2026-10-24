#!/usr/bin/env python3
"""
PEER'S Target Profiler - Automated Unit Test Suite
Day 05: OSINT + SE Target Profile Generator (Sqrock IT Solution)
Author: Md Peer Siddiqui
"""

import os
import sys
import json
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import target_profiler


class TestTargetProfiler(unittest.TestCase):

    def setUp(self):
        self.dossier_harish = target_profiler.OFFLINE_DOSSIERS["sqrock-engineer"]
        self.dossier_linus = target_profiler.OFFLINE_DOSSIERS["torvalds"]
        self.dossier_octocat = target_profiler.OFFLINE_DOSSIERS["octocat"]

    def test_offline_dossiers_exist_and_valid(self):
        """Verify that offline reference profiles exist with mandatory schema fields."""
        for key, d in target_profiler.OFFLINE_DOSSIERS.items():
            self.assertIn("login", d)
            self.assertIn("name", d)
            self.assertIn("company", d)
            self.assertIn("languages", d)
            self.assertIn("top_repositories", d)
            self.assertIsInstance(d["languages"], dict)
            self.assertIsInstance(d["top_repositories"], list)

    def test_opsec_score_bounds_and_tiering(self):
        """Verify OPSEC score is within [0, 100] and risk tiers are assigned properly."""
        opsec_harish = target_profiler.calculate_opsec_score(self.dossier_harish)
        self.assertGreaterEqual(opsec_harish["score"], 0)
        self.assertLessEqual(opsec_harish["score"], 100)
        self.assertIn(opsec_harish["tier"], ["LOW EXPOSURE", "MODERATE EXPOSURE", "HIGH EXPOSURE", "CRITICAL EXPOSURE"])
        self.assertTrue(len(opsec_harish["factors"]) >= 5)

        # Anonymous dummy profile test
        anon_profile = {"login": "ghost_dev", "public_repos": 0}
        opsec_anon = target_profiler.calculate_opsec_score(anon_profile)
        self.assertEqual(opsec_anon["score"], 0)
        self.assertEqual(opsec_anon["tier"], "LOW EXPOSURE")

    def test_spear_phishing_pretext_generation(self):
        """Ensure 3 tailored spear-phishing attack pretexts are synthesized."""
        scenarios = target_profiler.generate_spear_phishing_pretexts(self.dossier_harish)
        self.assertEqual(len(scenarios), 3)
        for s in scenarios:
            self.assertIn("id", s)
            self.assertIn("title", s)
            self.assertIn("vector", s)
            self.assertIn("hook", s)
            self.assertIn("call_to_action", s)
            self.assertIn("psychological_triggers", s)
            self.assertTrue(len(s["psychological_triggers"]) >= 2)

    def test_activity_timezone_analysis(self):
        """Verify activity hour distribution and inferred geographical region logic."""
        hours = [9, 10, 10, 10, 11, 14, 15]
        res = target_profiler.analyze_activity_timezones(hours)
        self.assertTrue(res["has_data"])
        self.assertEqual(res["peak_utc_hour"], 10)
        self.assertEqual(res["total_events_sampled"], 7)
        self.assertIn("Europe", res["inferred_region"])

        # Empty activity test
        empty_res = target_profiler.analyze_activity_timezones([])
        self.assertFalse(empty_res["has_data"])

    def test_json_deliverable_export(self):
        """Verify that target_profile.json exports correctly and matches required keys."""
        temp_out = os.path.join(target_profiler.TARGETS_DIR, "test_output.json")
        target_profiler.export_target_profile_json(self.dossier_harish, filepath=temp_out)
        self.assertTrue(os.path.exists(temp_out))

        with open(temp_out, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertIn("metadata", data)
        self.assertIn("target_profile", data)
        self.assertIn("adversary_intelligence", data)
        self.assertIn("defensive_opsec_evaluation", data)
        self.assertEqual(data["metadata"]["intern_name"], "Md Peer Siddiqui")
        self.assertEqual(data["metadata"]["organization"], "Sqrock IT Solution")

        if os.path.exists(temp_out):
            os.remove(temp_out)

    def test_email_harvesting_filtering(self):
        """Verify that commit email harvesting ignores noreply and extracts valid emails."""
        emails = self.dossier_harish.get("leaked_emails", [])
        self.assertTrue(any("@sqrock-labs.internal" in e for e in emails))
        self.assertFalse(any("noreply.github.com" in e for e in emails))

    def test_profile_empty_languages_fallback(self):
        """Ensure profile with no listed languages does not crash pretext generator."""
        empty_profile = {"login": "new_user", "name": "New User"}
        scenarios = target_profiler.generate_spear_phishing_pretexts(empty_profile)
        self.assertEqual(len(scenarios), 3)
        self.assertIn("Python", scenarios[0]["hook"])


if __name__ == "__main__":
    unittest.main()
