
import json
import os
from pathlib import Path
import requests

REPORT_FILE = Path("report-to-send.json")


def main():
    receiver_url = os.environ.get("RECEIVER_URL", "").rstrip("/")
    token = os.environ.get("REPORT_TOKEN", "")

    if not receiver_url or not token:
        raise SystemExit(
            "RECEIVER_URL and REPORT_TOKEN are required"
        )

    if not REPORT_FILE.exists():
        raise SystemExit("report-to-send.json not found")

    with REPORT_FILE.open(encoding="utf-8") as file:
        report = json.load(file)

    response = requests.post(
        receiver_url + "/report",
        json=report,
        headers={"X-Report-Token": token},
        timeout=30
    )

    response.raise_for_status()
    print("Report delivered successfully!")
    print("Receiver response:", response.text)


if __name__ == "__main__":
    main()
