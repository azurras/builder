from pathlib import Path
import json
import subprocess
import sys
import unittest
import urllib.error

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".agents/skills/deliver-change/scripts"))
import wait_for_github  # noqa: E402

REPOSITORY = "example/site.dev"
HEAD_COMMIT = "49700a7c0ffee000000000000000000000000000"


def check_run(name, status="COMPLETED", conclusion="SUCCESS", run_id="111"):
    return {"__typename": "CheckRun", "name": name, "status": status, "conclusion": conclusion,
            "detailsUrl": f"https://github.com/{REPOSITORY}/actions/runs/{run_id}/job/9"}


def pull_request_view(*checks, state="OPEN", merge_commit=None):
    return {"state": state, "headRefOid": HEAD_COMMIT, "statusCheckRollup": list(checks),
            "mergeCommit": {"oid": merge_commit} if merge_commit else None}


class FakeGitHub:
    """Serves successive `gh pr view` snapshots and records every other gh call."""

    def __init__(self, *views, merge_returncode=0):
        self.views = list(views)
        self.merge_returncode = merge_returncode
        self.calls = []

    def __call__(self, arguments):
        self.calls.append(arguments)
        if arguments[:2] == ["pr", "view"]:
            view = self.views.pop(0) if len(self.views) > 1 else self.views[0]
            return subprocess.CompletedProcess(arguments, 0, json.dumps(view), "")
        if arguments[:2] == ["pr", "merge"]:
            return subprocess.CompletedProcess(arguments, self.merge_returncode, "", "head moved")
        return subprocess.CompletedProcess(arguments, 0, "", "")

    def calls_starting(self, *prefix):
        return [call for call in self.calls if call[:len(prefix)] == list(prefix)]


class FakeClock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now

    def sleep(self, seconds):
        self.now += seconds


def wait_for(fake_github, *, merge_method=None, timeout_seconds=600):
    clock = FakeClock()
    return wait_for_github.wait_for_pull_request(REPOSITORY, 7, merge_method=merge_method,
                                                 timeout_seconds=timeout_seconds, interval_seconds=60,
                                                 run_command=fake_github, sleep=clock.sleep, clock=clock)


class PullRequestWaitTests(unittest.TestCase):
    def test_green_checks_merge_the_observed_head_then_report_the_merge(self):
        fake_github = FakeGitHub(pull_request_view(check_run("build", status="IN_PROGRESS", conclusion="")),
                                 pull_request_view(check_run("build")),
                                 pull_request_view(check_run("build"), state="MERGED", merge_commit="abc1234"))

        outcome = wait_for(fake_github, merge_method="squash")

        self.assertEqual(outcome.exit_code, 0, outcome.message)
        self.assertIn("merged as abc1234", outcome.message)
        self.assertEqual(fake_github.calls_starting("pr", "merge"),
                         [["pr", "merge", "7", "--repo", REPOSITORY, "--squash", "--match-head-commit", HEAD_COMMIT]])

    def test_without_merge_green_checks_finish_without_merging(self):
        fake_github = FakeGitHub(pull_request_view(check_run("build"), check_run("Analyze (java)")))

        outcome = wait_for(fake_github)

        self.assertEqual(outcome.exit_code, 0, outcome.message)
        self.assertIn("not merged", outcome.message)
        self.assertEqual(fake_github.calls_starting("pr", "merge"), [])

    def test_failed_check_is_named_and_never_merged(self):
        fake_github = FakeGitHub(pull_request_view(check_run("build", conclusion="FAILURE"), check_run("lint")))

        outcome = wait_for(fake_github, merge_method="squash")

        self.assertEqual(outcome.exit_code, 1)
        self.assertIn("failing checks: build", outcome.message)
        self.assertEqual(fake_github.calls_starting("pr", "merge"), [])

    def test_infrastructure_cancellation_is_rerun_once_then_treated_as_failure(self):
        cancelled = pull_request_view(check_run("build", conclusion="STARTUP_FAILURE", run_id="555"))
        fake_github = FakeGitHub(cancelled, cancelled)

        outcome = wait_for(fake_github, merge_method="squash")

        self.assertEqual(fake_github.calls_starting("run", "rerun"),
                         [["run", "rerun", "555", "--failed", "--repo", REPOSITORY]])
        self.assertEqual(outcome.exit_code, 1)
        self.assertIn("cancelled again after a re-run", outcome.message)

    def test_rerun_that_succeeds_lets_the_merge_proceed(self):
        fake_github = FakeGitHub(pull_request_view(check_run("build", conclusion="CANCELLED", run_id="555")),
                                 pull_request_view(check_run("build", status="QUEUED", conclusion="", run_id="555")),
                                 pull_request_view(check_run("build", run_id="555")),
                                 pull_request_view(check_run("build"), state="MERGED", merge_commit="abc1234"))

        outcome = wait_for(fake_github, merge_method="squash")

        self.assertEqual(outcome.exit_code, 0, outcome.message)
        self.assertEqual(len(fake_github.calls_starting("run", "rerun")), 1)

    def test_pending_checks_time_out_with_exit_two(self):
        fake_github = FakeGitHub(pull_request_view(check_run("build", status="IN_PROGRESS", conclusion="")))

        outcome = wait_for(fake_github, timeout_seconds=300)

        self.assertEqual(outcome.exit_code, 2)
        self.assertIn("Timed out", outcome.message)
        self.assertEqual(len(fake_github.calls_starting("pr", "view")), 6)

    def test_refused_merge_and_closed_pull_request_fail(self):
        refused = wait_for(FakeGitHub(pull_request_view(check_run("build")), merge_returncode=1), merge_method="squash")
        closed = wait_for(FakeGitHub(pull_request_view(check_run("build"), state="CLOSED")))

        self.assertEqual((refused.exit_code, closed.exit_code), (1, 1))
        self.assertIn("head moved", refused.message)
        self.assertIn("closed without merging", closed.message)

    def test_pull_request_with_no_checks_yet_keeps_waiting(self):
        fake_github = FakeGitHub(pull_request_view())

        outcome = wait_for(fake_github, timeout_seconds=120)

        self.assertEqual(outcome.exit_code, 2)


class LiveWaitTests(unittest.TestCase):
    def test_live_text_waits_through_errors_until_the_expected_commit_is_served(self):
        responses = [urllib.error.URLError("refused"), '{"git":{"commit":"1111111"}}', '{"git":{"commit":"49700a7"}}']

        def fetch(url):
            response = responses.pop(0)
            if isinstance(response, Exception):
                raise response
            return response

        clock = FakeClock()
        outcome = wait_for_github.wait_for_live_text("https://site.example/actuator/info", "49700a7",
                                                     timeout_seconds=600, interval_seconds=30, fetch=fetch,
                                                     sleep=clock.sleep, clock=clock)

        self.assertEqual(outcome.exit_code, 0, outcome.message)
        self.assertEqual(clock.now, 60)

    def test_live_text_times_out_naming_the_last_problem(self):
        clock = FakeClock()
        outcome = wait_for_github.wait_for_live_text("https://site.example/", "49700a7", timeout_seconds=60,
                                                     interval_seconds=30, fetch=lambda url: "old build",
                                                     sleep=clock.sleep, clock=clock)

        self.assertEqual(outcome.exit_code, 2)
        self.assertIn("did not contain 49700a7", outcome.message)


if __name__ == "__main__":
    unittest.main()
