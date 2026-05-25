from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


def test_get_activities_returns_activity_catalog():
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()

    assert "Chess Club" in data
    assert "Programming Class" in data
    assert data["Chess Club"]["participants"]


def test_signup_adds_participant_and_persists():
    email = "signup-test@example.edu"

    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"

    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]


def test_signup_rejects_duplicate_participant():
    email = "duplicate-test@example.edu"

    first_response = client.post("/activities/Chess Club/signup", params={"email": email})
    second_response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_removes_participant():
    email = "unregister-test@example.edu"

    client.post("/activities/Chess Club/signup", params={"email": email})

    delete_response = client.delete("/activities/Chess Club/signup", params={"email": email})

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == f"Unregistered {email} from Chess Club"

    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_unknown_participant_returns_404():
    response = client.delete("/activities/Chess Club/signup", params={"email": "missing@example.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
