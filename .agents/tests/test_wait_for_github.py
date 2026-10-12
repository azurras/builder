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


class BehindBranchTests(unittest.TestCase):
    def test_behind_branch_is_updated_once_per_head_and_merged_only_when_current(self):
        behind = dict(pull_request_view(check_run("build")), mergeStateStatus="BEHIND")
        current = dict(pull_request_view(check_run("build")), mergeStateStatus="CLEAN")
        fake_github = FakeGitHub(behind, behind, current,
                                 pull_request_view(check_run("build"), state="MERGED", merge_commit="abc1234"))

        outcome = wait_for(fake_github, merge_method="squash")

        self.assertEqual(outcome.exit_code, 0, outcome.message)
        self.assertEqual(fake_github.calls_starting("pr", "update-branch"),
                         [["pr", "update-branch", "7", "--repo", REPOSITORY]])
        self.assertEqual(len(fake_github.calls_starting("pr", "merge")), 1)
        self.assertEqual(outcome.merge_commit, "abc1234")


MAIN_HEAD = "a" * 40
NEXT_HEAD = "b" * 40
AUTO_DEPLOY = wait_for_github.AutoDeploy("https://site.example/actuator/info",
                                         wait_for_github.re.compile(r"-dev\.([0-9a-f]{40})"))


def info_body(commit):
    return json.dumps({"build": {"version": f"0.0.0-dev.{commit}"}})


class FakeProduction:
    """Serves the live commit and answers the GitHub API calls the deploy-aware modes make."""

    def __init__(self, live_commits, *, heads=(MAIN_HEAD,), compare_status="ahead", pull_requests=None):
        self.live_commits = list(live_commits)
        self.heads = list(heads)
        self.compare_status = compare_status
        self.pull_requests = pull_requests or {}
        self.calls = []

    def fetch(self, url):
        commit = self.live_commits.pop(0) if len(self.live_commits) > 1 else self.live_commits[0]
        self.calls.append(["live", commit])
        return info_body(commit)

    def __call__(self, arguments):
        self.calls.append(arguments)
        if arguments[0] == "api" and "/commits/" in arguments[1]:
            head = self.heads.pop(0) if len(self.heads) > 1 else self.heads[0]
            return subprocess.CompletedProcess(arguments, 0, head + "\n", "")
        if arguments[0] == "api" and "/compare/" in arguments[1]:
            return subprocess.CompletedProcess(arguments, 0, self.compare_status + "\n", "")
        if arguments[:2] == ["pr", "view"]:
            views = self.pull_requests[arguments[2]]
            view = views.pop(0) if len(views) > 1 else views[0]
            return subprocess.CompletedProcess(arguments, 0, json.dumps(view), "")
        return subprocess.CompletedProcess(arguments, 0, "", "")


class DeployedWaitTests(unittest.TestCase):
    def deployed(self, production, commit, timeout_seconds=600):
        clock = FakeClock()
        return wait_for_github.wait_for_deployed_commit(REPOSITORY, AUTO_DEPLOY, commit,
                                                        timeout_seconds=timeout_seconds, interval_seconds=60,
                                                        run_command=production, fetch=production.fetch,
                                                        sleep=clock.sleep, clock=clock)

    def test_exact_live_commit_needs_no_compare(self):
        production = FakeProduction([MAIN_HEAD])

        outcome = self.deployed(production, MAIN_HEAD[:7])

        self.assertEqual(outcome.exit_code, 0, outcome.message)
        self.assertFalse([call for call in production.calls if call[0] == "api"])

    def test_a_later_live_commit_that_contains_the_merge_counts_as_live(self):
        production = FakeProduction([NEXT_HEAD], compare_status="ahead")

        outcome = self.deployed(production, MAIN_HEAD)

        self.assertEqual(outcome.exit_code, 0, outcome.message)
        self.assertIn(["api", f"repos/{REPOSITORY}/compare/{MAIN_HEAD}...{NEXT_HEAD}", "--jq", ".status"],
                      production.calls)

    def test_an_older_live_commit_times_out_naming_what_production_serves(self):
        production = FakeProduction([NEXT_HEAD], compare_status="behind")

        outcome = self.deployed(production, MAIN_HEAD, timeout_seconds=120)

        self.assertEqual(outcome.exit_code, 2)
        self.assertIn(f"production still serves {NEXT_HEAD[:7]}", outcome.message)


class MergeQueueTests(unittest.TestCase):
    def test_each_pr_waits_for_production_to_serve_the_previous_merge(self):
        green = dict(pull_request_view(check_run("build")), mergeStateStatus="CLEAN")
        production = FakeProduction(
            ["0" * 40, MAIN_HEAD, MAIN_HEAD, MAIN_HEAD, NEXT_HEAD, NEXT_HEAD],
            heads=(MAIN_HEAD, MAIN_HEAD, NEXT_HEAD, NEXT_HEAD, NEXT_HEAD),
            pull_requests={"7": [green, pull_request_view(check_run("build"), state="MERGED", merge_commit=NEXT_HEAD)],
                           "8": [green, pull_request_view(check_run("build"), state="MERGED", merge_commit="c" * 40)]})
        production.compare_status = "identical"
        clock = FakeClock()

        outcome = wait_for_github.merge_queue(REPOSITORY, "main", AUTO_DEPLOY, [7, 8], merge_method="squash",
                                              timeout_seconds=900, interval_seconds=60, run_command=production,
                                              fetch=production.fetch, sleep=clock.sleep, clock=clock)

        self.assertEqual(outcome.exit_code, 0, outcome.message)
        merges = [index for index, call in enumerate(production.calls) if call[:2] == ["pr", "merge"]]
        self.assertEqual([production.calls[index][2] for index in merges], ["7", "8"])
        live_before_second_merge = [call[1] for call in production.calls[:merges[1]] if call[0] == "live"]
        self.assertEqual(live_before_second_merge[-1], NEXT_HEAD)
        self.assertEqual(outcome.merge_commit, "c" * 40)

    def test_a_failed_pr_stops_the_queue_before_later_prs(self):
        failed = pull_request_view(check_run("build", conclusion="FAILURE"))
        production = FakeProduction([MAIN_HEAD], pull_requests={"7": [failed], "8": [failed]})
        clock = FakeClock()

        outcome = wait_for_github.merge_queue(REPOSITORY, "main", AUTO_DEPLOY, [7, 8], merge_method="squash",
                                              timeout_seconds=900, interval_seconds=60, run_command=production,
                                              fetch=production.fetch, sleep=clock.sleep, clock=clock)

        self.assertEqual(outcome.exit_code, 1)
        self.assertFalse([call for call in production.calls if call[:3] == ["pr", "view", "8"]])


class GitHubRepositoryTests(unittest.TestCase):
    def test_registered_remotes_resolve_to_owner_and_name(self):
        self.assertEqual(wait_for_github.github_repository_of("https://github.com/azurras/site.dev.git"),
                         "azurras/site.dev")
        self.assertEqual(wait_for_github.github_repository_of("git@github.com:azurras/site.dev.git"),
                         "azurras/site.dev")
        with self.assertRaises(ValueError):
            wait_for_github.github_repository_of("https://gitlab.com/azurras/site.dev.git")


if __name__ == "__main__":
    unittest.main()
