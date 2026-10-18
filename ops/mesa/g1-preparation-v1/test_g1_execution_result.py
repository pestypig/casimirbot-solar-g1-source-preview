import unittest
from g1_execution_result import classify_execution


class ExecutionResultTests(unittest.TestCase):
    def complete(self, **changes):
        args = dict(exit_code=0, outputs_present=True, outputs_fresh=True,
                    provenance_complete=True, reached_target_age=True,
                    expected_termination=True)
        args.update(changes)
        return classify_execution(**args)

    def test_complete_only_unlocks_extraction(self):
        result = self.complete()
        self.assertTrue(result["extractionAllowed"])
        self.assertFalse(result["admissionAllowed"])

    def test_failures_reject_before_fit(self):
        cases = [("timed_out", True, "BLOCK_TIMEOUT"),
                 ("oom_killed", True, "BLOCK_OOM"),
                 ("exit_code", 1, "BLOCK_EXIT_STATUS"),
                 ("outputs_present", False, "BLOCK_MISSING_OUTPUTS"),
                 ("outputs_fresh", False, "BLOCK_STALE_OUTPUTS"),
                 ("provenance_complete", False, "BLOCK_PROVENANCE"),
                 ("expected_termination", False, "BLOCK_TERMINATION"),
                 ("reached_target_age", False, "BLOCK_TARGET_AGE")]
        for key, value, expected in cases:
            with self.subTest(key=key):
                result = self.complete(**{key: value})
                self.assertEqual(result["status"], expected)
                self.assertFalse(result["extractionAllowed"])

    def test_missing_and_wrong_types_fail_closed(self):
        self.assertFalse(classify_execution(exit_code=0)["extractionAllowed"])
        for value in (True, "0", None, 0.0):
            self.assertEqual(self.complete(exit_code=value)["status"], "BLOCK_EXIT_STATUS")
        self.assertEqual(self.complete(outputs_fresh="yes")["status"],
                         "BLOCK_INVALID_EXECUTION_EVIDENCE")

    def test_timeout_wins_over_other_failures(self):
        self.assertEqual(self.complete(timed_out=True, oom_killed=True,
                                     exit_code=137)["status"], "BLOCK_TIMEOUT")
