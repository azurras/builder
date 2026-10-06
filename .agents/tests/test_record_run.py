from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".agents/skills/write-test-report/scripts/record_run.py"
sys.path.insert(0, str(ROOT / ".agents/lib"))
from artifact_quality import validate_test_report_text  # noqa: E402


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        status, body = (200, b'{"status":"UP"}') if self.path == "/health" else (404, b'{"error":"missing"}')
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Set-Cookie", "session=abc123")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


class RecordRunTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name).resolve()
        self.evidence = self.workspace / "evidence.jsonl"
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), HealthHandler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        self.base_url = f"http://127.0.0.1:{self.server.server_address[1]}"

    def record(self, *args):
        return subprocess.run([sys.executable, "-B", str(SCRIPT), *args], capture_output=True, text=True,
                              encoding="utf-8", timeout=60)

    def render(self):
        return self.record("render", "--evidence", str(self.evidence), "--title", "Health endpoint",
                           "--story", "Health check returns UP", "--branch", "claude/health-20261005",
                           "--project", "builder", "--env", "Port=ephemeral")

    def test_passing_cases_render_a_complete_report_the_validator_accepts(self):
        http_result = self.record("http", "--evidence", str(self.evidence), "--case", "Health is UP",
                                  "--url", f"{self.base_url}/health", "--expect-text", '"UP"',
                                  "--header", "Authorization: Bearer secret-token-value")
        command_result = self.record("run", "--evidence", str(self.evidence), "--case", "CLI prints version",
                                     "--cwd", str(self.workspace), "--", sys.executable, "-c", "print('app 1.2.3')")

        report = self.render()

        self.assertEqual((http_result.returncode, command_result.returncode), (0, 0),
                         http_result.stdout + http_result.stderr + command_result.stderr)
        self.assertEqual(report.returncode, 0, report.stderr)
        self.assertEqual(validate_test_report_text(report.stdout), [])
        self.assertIn("2 of 2 cases passed", report.stdout)
        self.assertIn("## Document Status\ncomplete", report.stdout)
        self.assertIn("app 1.2.3", report.stdout)
        self.assertIn('{"status":"UP"}', report.stdout)
        self.assertNotIn("secret-token-value", self.evidence.read_text(encoding="utf-8"))
        self.assertNotIn("abc123", self.evidence.read_text(encoding="utf-8"))

    def test_failed_case_exits_one_and_renders_a_draft_naming_the_failure(self):
        missing = self.record("http", "--evidence", str(self.evidence), "--case", "Missing page",
                              "--url", f"{self.base_url}/missing", "--expect-status", "200")
        crashed = self.record("run", "--evidence", str(self.evidence), "--case", "Crashing command",
                              "--", sys.executable, "-c", "import sys; sys.exit(3)")

        report = self.render()

        self.assertEqual((missing.returncode, crashed.returncode), (1, 1))
        self.assertIn("0 of 2 cases passed", report.stdout)
        self.assertIn("## Document Status\ndraft", report.stdout)
        self.assertIn("Case 1 (Missing page) failed: expected status 200.", report.stdout)
        self.assertIn("exit code: 3", report.stdout)

    def test_unreachable_server_is_recorded_as_a_failure(self):
        self.server.shutdown()
        self.server.server_close()

        result = self.record("http", "--evidence", str(self.evidence), "--case", "Server down",
                             "--url", f"{self.base_url}/health", "--timeout-seconds", "5")

        self.assertEqual(result.returncode, 1)
        self.assertIn("no response", self.evidence.read_text(encoding="utf-8"))

    def test_bad_input_and_empty_evidence_exit_two(self):
        self.assertEqual(self.record("run", "--evidence", str(self.evidence), "--case", "Nothing").returncode, 2)
        self.assertEqual(self.record("http", "--evidence", str(self.evidence), "--case", "x",
                                     "--url", "ftp://example").returncode, 2)
        self.evidence.write_text("", encoding="utf-8")
        self.assertEqual(self.render().returncode, 2)


if __name__ == "__main__":
    unittest.main()
