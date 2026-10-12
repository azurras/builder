from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".agents/skills/verify-local-app/scripts/compare_responses.py"

ROUTES = {
    "/candidate/info": (200, "application/json", {"build": {"version": "1", "tags": ["a"]}, "timestamp": "t1"}),
    "/reference/info": (200, "application/json", {"build": {"version": "2", "tags": []}, "timestamp": "t2"}),
    "/candidate/denied": (403, "application/json", {"status": 403, "error": "Forbidden", "timestamp": "t1"}),
    "/reference/denied": (403, "application/json", {"status": 403, "error": "Forbidden", "timestamp": "t2"}),
    "/candidate/robots.txt": (200, "text/plain", "User-agent: *\nDisallow: /api/\n"),
    "/reference/robots.txt": (200, "text/plain", "User-agent: *\nDisallow: /\n"),
}


class Handler(BaseHTTPRequestHandler):
    seen_headers = []

    def do_GET(self):
        Handler.seen_headers.append((self.headers.get("Accept"), self.headers.get("User-Agent")))
        status, content_type, body = ROUTES.get(self.path, (404, "text/plain", "missing"))
        payload = body.encode() if isinstance(body, str) else json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format, *args):
        pass


class CompareResponsesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.base = f"http://127.0.0.1:{cls.server.server_address[1]}"
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def run_script(self, *arguments):
        return subprocess.run([sys.executable, str(SCRIPT), *arguments], capture_output=True, text=True,
                              encoding="utf-8", timeout=60, check=False)

    def saved_json(self, value):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / "expected.json"
        path.write_text(json.dumps(value), encoding="utf-8")
        return str(path)

    def test_shape_matches_when_only_values_differ(self):
        expected = self.saved_json({"build": {"version": "9", "tags": []}, "timestamp": None})

        completed = self.run_script("shape", "--url", self.base + "/candidate/info", "--expected-file", expected)

        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("shape matches", completed.stdout)

    def test_shape_names_missing_unexpected_and_retyped_keys(self):
        expected = self.saved_json({"build": {"version": 9, "commit": "x"}, "timestamp": "t"})

        completed = self.run_script("shape", "--url", self.base + "/candidate/info", "--expected-file", expected)

        self.assertEqual(completed.returncode, 1)
        for difference in ("$.build.commit missing", "$.build.tags unexpected", "$.build.version int != str"):
            self.assertIn(difference, completed.stdout)

    def test_same_ignores_the_timestamp_and_compares_error_statuses_as_data(self):
        completed = self.run_script("same", "--candidate", self.base + "/candidate/denied",
                                    "--reference", self.base + "/reference/denied", "--expect-status", "403")

        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertTrue(completed.stdout.rstrip().endswith("same"))

    def test_same_reports_different_bodies_and_an_unexpected_status(self):
        different_text = self.run_script("same", "--candidate", self.base + "/candidate/robots.txt",
                                         "--reference", self.base + "/reference/robots.txt",
                                         "--expect-status", "200", "--accept", "text/plain")
        wrong_status = self.run_script("same", "--candidate", self.base + "/candidate/denied",
                                       "--reference", self.base + "/reference/denied", "--expect-status", "200")

        self.assertEqual((different_text.returncode, wrong_status.returncode), (1, 1))
        self.assertTrue(different_text.stdout.rstrip().endswith("different"))

    def test_requests_send_the_accept_header_and_a_non_default_user_agent(self):
        Handler.seen_headers.clear()

        self.run_script("same", "--candidate", self.base + "/candidate/robots.txt",
                        "--reference", self.base + "/candidate/robots.txt", "--expect-status", "200",
                        "--accept", "text/plain")

        self.assertEqual(Handler.seen_headers, [("text/plain", "builder-verify-local-app")] * 2)

    def test_unreachable_host_exits_two(self):
        completed = self.run_script("same", "--candidate", "http://127.0.0.1:9/", "--reference",
                                    self.base + "/reference/denied", "--expect-status", "403")

        self.assertEqual(completed.returncode, 2)
        self.assertIn("could not run", completed.stderr)


if __name__ == "__main__":
    unittest.main()
