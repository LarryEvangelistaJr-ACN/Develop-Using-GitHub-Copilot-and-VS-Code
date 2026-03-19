from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    # Arrange - no setup needed

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_success():
    # Arrange
    email = "signup_success@example.com"

    # Act
    response = client.post("/activities/Chess%20Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert "Signed up" in result["message"]

    # Verify participant was added
    response2 = client.get("/activities")
    data = response2.json()
    assert email in data["Chess Club"]["participants"]


def test_signup_duplicate():
    # Arrange
    email = "signup_duplicate@example.com"
    client.post("/activities/Chess%20Club/signup", params={"email": email})  # First signup

    # Act
    response = client.post("/activities/Chess%20Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert "already signed up" in result["detail"]


def test_remove_participant_success():
    # Arrange
    email = "remove_success@example.com"
    client.post("/activities/Chess%20Club/signup", params={"email": email})  # Ensure exists

    # Act
    response = client.delete("/activities/Chess%20Club/participants", params={"email": email})

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert "Removed" in result["message"]

    # Verify participant was removed
    response2 = client.get("/activities")
    data = response2.json()
    assert email not in data["Chess Club"]["participants"]


def test_remove_participant_not_found():
    # Arrange
    email = "remove_not_found@example.com"

    # Act
    response = client.delete("/activities/Chess%20Club/participants", params={"email": email})

    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert "not found" in result["detail"]


def test_signup_activity_not_found():
    # Arrange
    email = "activity_not_found@example.com"

    # Act
    response = client.post("/activities/NonExistent/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert "not found" in result["detail"]