
import pytest
import app as app_module


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Use a separate temporary file for each test
    monkeypatch.setattr(
        app_module,
        "SUBMISSIONS_FILE",
        str(tmp_path / "test_submissions.json")
    )

    app_module.app.config["TESTING"] = True

    with app_module.app.test_client() as test_client:
        yield test_client


# Test 1: Valid submission
def test_valid_submission(client):
    response = client.post("/submit", json={
        "name": "Test Student",
        "reg_number": "FA23-BAI-001",
        "title": "DevOps Lab Mid",
        "url": "https://github.com/afrah-21"
    })

    assert response.status_code == 201
    assert response.get_json()["success"] is True

    submissions = client.get("/submissions").get_json()

    assert len(submissions) == 1
    assert submissions[0]["reg_number"] == "FA23-BAI-001"


# Test 2: Missing registration number
def test_missing_registration_number(client):
    response = client.post("/submit", json={
        "name": "Test Student",
        "reg_number": "",
        "title": "DevOps Lab Mid",
        "url": "https://github.com/afrah-21"
    })

    assert response.status_code == 400
    assert response.get_json()["success"] is False
    assert "registration" in response.get_json()["message"].lower()

    submissions = client.get("/submissions").get_json()
    assert len(submissions) == 0


# Test 3: Invalid submission URL
def test_invalid_url(client):
    response = client.post("/submit", json={
        "name": "Test Student",
        "reg_number": "FA23-BAI-002",
        "title": "DevOps Lab Mid",
        "url": "invalid-url"
    })

    assert response.status_code == 400
    assert response.get_json()["success"] is False

    submissions = client.get("/submissions").get_json()
    assert len(submissions) == 0
