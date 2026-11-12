# DevOps Assignment Submission Portal

## Project Overview

This project is an Assignment Submission Portal developed using Python, Flask, HTML, and GitHub Actions.

It demonstrates Continuous Integration (CI), automated testing, JSON test report generation, delivery to a local receiver, GitHub Pages deployment, and automatic email reporting.

## Technologies Used

- Python 3.11
- Flask
- HTML and CSS
- Pytest
- Git and GitHub
- GitHub Actions
- JSON
- ngrok
- Gmail SMTP

## Project Features

### 1. Assignment Submission Portal
Students can submit assignment information using a web form. The Flask application validates the input and stores submitted records.

### 2. Automated Testing
Pytest automatically checks the application's functionality.

### 3. CI/CD Pipeline
GitHub Actions runs the automated tests when code is pushed to the repository.

### 4. JSON Test Reporting
The pipeline generates a JSON report containing test results and execution details.

### 5. Local Report Receiver
The generated report is sent through ngrok to a local Python receiver.

### 6. GitHub Pages Deployment
The project's static frontend is deployed automatically to GitHub Pages after successful CI checks.

### 7. Automatic Email Reporting
GitHub Actions sends the test report by email with the JSON file attached.

### 8. CI Failure Detection
The project demonstrates how GitHub Actions detects a failing test and verifies that the pipeline passes after the test is corrected.

## Repository Structure

```text
assignment-portal/
├── .github/workflows/ci.yml
├── docs/index.html
├── static/index.html
├── tests/test_portal.py
├── app.py
├── receiver.py
├── generate_report.py
├── send_report.py
├── email_report.py
├── requirements.txt
└── README.md
```

## Run the Project Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the Flask application:

```bash
python app.py
```

Open:

`http://127.0.0.1:5000`

Run automated tests:

```bash
python -m pytest tests/test_portal.py -v
```

## GitHub Actions Workflow

The CI/CD pipeline performs these tasks:

1. Checks out the repository.
2. Configures Python.
3. Installs dependencies.
4. Runs automated tests.
5. Generates a JSON test report.
6. Uploads the report as a workflow artifact.
7. Sends the report to the local receiver.
8. Sends an email with the JSON report attached.
9. Verifies test results.
10. Deploys the static frontend to GitHub Pages when CI succeeds.

## Live Website

https://afrah-21.github.io/assignment-portal/

Note: GitHub Pages hosts the static frontend. The Flask backend runs separately.

## GitHub Repository

https://github.com/afrah-21/assignment-portal

## Project Status

The project has demonstrated successful automated testing, failure detection, JSON reporting, local receiver delivery, GitHub Pages deployment, and email delivery.