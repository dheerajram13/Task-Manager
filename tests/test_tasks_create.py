from datetime import date, timedelta


def future_date(days: int = 3) -> str:
    return (date.today() + timedelta(days=days)).isoformat()


def past_date(days: int = 1) -> str:
    return (date.today() - timedelta(days=days)).isoformat()


def test_create_task_success(client):
    payload = {
        "title": "Prepare sprint board",
        "description": "Create and organize sprint tasks",
        "priority": 5,
        "due_date": future_date(),
        "tags": ["Work", "Urgent"],
    }

    response = client.post("/tasks", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Prepare sprint board"
    assert data["priority"] == 5
    assert data["tags"] == ["work", "urgent"]


def test_create_task_priority_validation_failure(client):
    payload = {
        "title": "Invalid priority",
        "priority": 9,
        "due_date": future_date(),
        "tags": ["work"],
    }

    response = client.post("/tasks", json=payload)

    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "Validation Failed"
    assert "priority" in data["details"]


def test_create_task_due_date_in_past_validation_failure(client):
    payload = {
        "title": "Past due date",
        "priority": 3,
        "due_date": past_date(),
        "tags": ["work"],
    }

    response = client.post("/tasks", json=payload)

    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "Validation Failed"
    assert data["details"]["due_date"] == "Must not be in the past"
