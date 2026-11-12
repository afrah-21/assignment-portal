
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import json
import os
import hmac

BASE_DIR = Path(__file__).resolve().parent
REPORT_FILE = BASE_DIR / "test-report.json"
REPORT_TOKEN = os.environ.get("REPORT_TOKEN", "")


class ReportHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path != "/report":
            self.send_error(404, "Not found")
            return

        if not REPORT_TOKEN:
            self.send_error(503, "Receiver token not configured")
            return

        received_token = self.headers.get("X-Report-Token", "")

        if not hmac.compare_digest(received_token, REPORT_TOKEN):
            self.send_error(401, "Unauthorized")
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))

            if length <= 0 or length > 1024 * 1024:
                self.send_error(413, "Invalid report size")
                return

            body = self.rfile.read(length)
            report = json.loads(body)

            required = [
                "repository", "branch", "commit_sha",
                "run_id", "timestamp", "tests",
                "total_count", "passed_count",
                "failed_count", "overall_status"
            ]

            if not isinstance(report, dict) or any(
                key not in report for key in required
            ):
                self.send_error(400, "Invalid report format")
                return

            if not isinstance(report["tests"], list):
                self.send_error(400, "Invalid tests list")
                return

            with open(REPORT_FILE, "w", encoding="utf-8") as file:
                json.dump(report, file, indent=4)

            print("\nREPORT RECEIVED SUCCESSFULLY!")
            print("Repository:", report["repository"])
            print("Commit:", report["commit_sha"])
            print("Status:", report["overall_status"])
            print("Passed:", report["passed_count"])
            print("Failed:", report["failed_count"])
            print("Saved to:", REPORT_FILE)

            response = json.dumps({"status": "saved"}).encode()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

        except (ValueError, json.JSONDecodeError):
            self.send_error(400, "Invalid JSON")
        except Exception as error:
            print("Receiver error:", error)
            self.send_error(500, "Server error")


if __name__ == "__main__":
    if not REPORT_TOKEN:
        raise SystemExit(
            "Set REPORT_TOKEN before starting receiver.py"
        )

    server = HTTPServer(("127.0.0.1", 5001), ReportHandler)

    print("Local report receiver is running!")
    print("URL: http://127.0.0.1:5001/report")
    print("Saving reports to:", REPORT_FILE)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nReceiver stopped.")
    finally:
        server.server_close()
