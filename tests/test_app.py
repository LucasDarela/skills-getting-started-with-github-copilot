from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_signup_for_activity_adds_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    activity_before = client.get("/activities").json()[activity_name]

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for {activity_name}"
    }

    activity_after = client.get("/activities").json()[activity_name]
    assert email in activity_after["participants"]
    assert email not in activity_before["participants"]


def test_unregister_participant_removes_member_from_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={email}"
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from {activity_name}"
    }

    activity = client.get("/activities").json()[activity_name]
    assert email not in activity["participants"]
