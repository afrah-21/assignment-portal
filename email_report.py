
import os
import json
import smtplib
import ssl
from pathlib import Path
from email.message import EmailMessage

report = json.loads(
    Path("report-to-send.json").read_text(encoding="utf-8")
)

sender = os.environ["SMTP_USERNAME"]
password = os.environ["SMTP_PASSWORD"]
recipient = os.environ["REPORT_EMAIL"]

status = report["overall_status"].upper()

message = EmailMessage()
message["From"] = sender
message["To"] = recipient
message["Subject"] = f"DevOps CI Report - {status}"

message.set_content(f"""
DevOps Automated Test Report

Repository: {report['repository']}
Branch: {report['branch']}
Commit: {report['commit_sha']}
Run ID: {report['run_id']}
Timestamp: {report['timestamp']}

Total Tests: {report['total_count']}
Passed: {report['passed_count']}
Failed: {report['failed_count']}

Overall Status: {status}

Test Details:
""" + "\n".join(
    f"{t['name']}: {t['result']}\n"
    f"{t.get('failure_message', '')}"
    for t in report["tests"]
))

with open("report-to-send.json", "rb") as file:
    message.add_attachment(
        file.read(),
        maintype="application",
        subtype="json",
        filename="test-report.json"
    )

context = ssl.create_default_context()

with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
    server.ehlo()
    server.starttls(context=ssl.create_default_context())
    server.ehlo()
    server.login(sender, password)
    server.send_message(message)

print("Email report sent successfully!")