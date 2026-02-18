from datetime import date, timedelta


def future_date(days: int = 3) -> str:
    return (date.today() + timedelta(days=days)).isoformat()


def past_date(days: int = 1) -> str:
    return (date.today() - timedelta(days=days)).isoformat()


def create_task(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Patch target",
            "description": "before",
            "priority": 3,
            "due_date": future_date(5),
            "tags": ["work"],
        },
    )
    assert response.status_code == 201
    return response.json()


def test_patch_task_partial_update(client):
    created = create_task(client)

    response = client.patch(
        f"/tasks/{created['id']}",
        json={"title": "Patched title"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Patched title"
    assert data["description"] == "before"
    assert data["priority"] == 3


def test_patch_task_validation_failure_for_past_due_date(client):
    created = create_task(client)

    response = client.patch(
        f"/tasks/{created['id']}",
        json={"due_date": past_date()},
    )

    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "Validation Failed"
    assert data["details"]["due_date"] == "Must not be in the past"


def test_patch_task_empty_body_validation_failure(client):
    created = create_task(client)

    response = client.patch(f"/tasks/{created['id']}", json={})

    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "Validation Failed"
    assert data["details"]["body"] == "At least one field must be provided"
