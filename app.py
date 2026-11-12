
from flask import Flask, request, jsonify, send_from_directory
import json
import os
import re

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SUBMISSIONS_FILE = os.path.join(BASE_DIR, "submissions.json")


def load_submissions():
    if os.path.exists(SUBMISSIONS_FILE):
        with open(SUBMISSIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_submissions(submissions):
    with open(SUBMISSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(submissions, f, indent=4)


def is_valid_url(url):
    pattern = re.compile(
        r"^https?://"
        r"(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}"
        r"(?::\d+)?(?:[/?#]\S*)?$"
    )
    return bool(pattern.fullmatch(url))


@app.route("/")
def home():
    return send_from_directory("static", "index.html")


@app.route("/submit", methods=["POST"])
def submit_assignment():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "message": "Valid JSON data is required"
        }), 400

    name = data.get("name", "")
    reg_number = data.get("reg_number", "")
    title = data.get("title", "")
    url = data.get("url", "")

    if not all(isinstance(v, str) for v in
               [name, reg_number, title, url]):
        return jsonify({
            "success": False,
            "message": "All fields must be text"
        }), 400

    name = name.strip()
    reg_number = reg_number.strip()
    title = title.strip()
    url = url.strip()

    if not name:
        return jsonify({
            "success": False,
            "message": "Student name is required"
        }), 400

    if not reg_number:
        return jsonify({
            "success": False,
            "message": "Registration number is required"
        }), 400

    if not title:
        return jsonify({
            "success": False,
            "message": "Assignment title is required"
        }), 400

    if not url:
        return jsonify({
            "success": False,
            "message": "Submission URL is required"
        }), 400

    if not is_valid_url(url):
        return jsonify({
            "success": False,
            "message": "Invalid submission URL"
        }), 400

    submission = {
        "name": name,
        "reg_number": reg_number,
        "title": title,
        "url": url
    }

    submissions = load_submissions()
    submissions.append(submission)
    save_submissions(submissions)

    return jsonify({
        "success": True,
        "message": "Assignment submitted successfully!"
    }), 201


@app.route("/submissions", methods=["GET"])
def get_submissions():
    return jsonify(load_submissions())


if __name__ == "__main__":
    app.run(debug=True, port=5000)
