
import json
import os
from pathlib import Path
from datetime import datetime, timezone

SOURCE = Path("pytest-results.json")
DESTINATION = Path("report-to-send.json")


def main():
    if not SOURCE.exists():
        raise SystemExit("pytest-results.json is missing")

    with SOURCE.open(encoding="utf-8") as file:
        pytest_report = json.load(file)

    tests = []

    for test in pytest_report.get("tests", []):
        outcome = test.get("outcome", "unknown")
        failure_message = ""

        if outcome == "failed":
            for phase in ("setup", "call", "teardown"):
                details = test.get(phase, {})
                if details.get("outcome") == "failed":
                    failure_message = str(
                        details.get("longrepr", "Test failed")
                    )
                    break

        tests.append({
            "name": test.get("nodeid", "unknown"),
            "result": outcome,
            "failure_message": failure_message
        })

    summary = pytest_report.get("summary", {})
    total = len(tests)
    passed = sum(t["result"] == "passed" for t in tests)
    failed = sum(t["result"] == "failed" for t in tests)

    overall_status = (
        "passed"
        if total > 0
        and failed == 0
        and passed == total
        and not pytest_report.get("exitcode", 1)
        else "failed"
    )

    report = {
        "repository": os.getenv(
            "GITHUB_REPOSITORY", "afrah-21/assignment-portal"
        ),
        "branch": os.getenv("GITHUB_REF_NAME", "local"),
        "commit_sha": os.getenv("GITHUB_SHA", "local"),
        "run_id": os.getenv("GITHUB_RUN_ID", "local"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tests": tests,
        "total_count": total,
        "passed_count": passed,
        "failed_count": failed,
        "overall_status": overall_status
    }

    with DESTINATION.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print("JSON report generated:", DESTINATION)
    print("Total:", total)
    print("Passed:", passed)
    print("Failed:", failed)
    print("Overall status:", overall_status)


if __name__ == "__main__":
    main()
