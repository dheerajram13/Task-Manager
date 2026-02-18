from datetime import date, timedelta


def future_date(days: int) -> str:
    return (date.today() + timedelta(days=days)).isoformat()


def create_task(client, *, title: str, priority: int, tags: list[str]):
    response = client.post(
        "/tasks",
        json={
            "title": title,
            "priority": priority,
            "due_date": future_date(5),
            "tags": tags,
        },
    )
    assert response.status_code == 201
    return response.json()


def test_filter_tasks_by_priority_and_tags(client):
    task1 = create_task(client, title="A", priority=5, tags=["work", "urgent"])
    task2 = create_task(client, title="B", priority=3, tags=["home"])
    create_task(client, title="C", priority=5, tags=["personal"])

    priority_response = client.get("/tasks", params={"priority": 5})
    assert priority_response.status_code == 200
    priority_data = priority_response.json()
    assert priority_data["total"] == 2

    tags_response = client.get("/tasks", params={"tags": "urgent,home"})
    assert tags_response.status_code == 200
    tags_data = tags_response.json()
    assert tags_data["total"] == 2
    item_ids = {item["id"] for item in tags_data["items"]}
    assert task1["id"] in item_ids
    assert task2["id"] in item_ids


def test_filter_tasks_by_completed_and_pagination(client):
    first = create_task(client, title="Task 1", priority=2, tags=["alpha"])
    second = create_task(client, title="Task 2", priority=2, tags=["beta"])
    create_task(client, title="Task 3", priority=2, tags=["gamma"])

    patch_response = client.patch(
        f"/tasks/{second['id']}",
        json={"completed": True},
    )
    assert patch_response.status_code == 200

    completed_response = client.get("/tasks", params={"completed": "true"})
    assert completed_response.status_code == 200
    completed_data = completed_response.json()
    assert completed_data["total"] == 1
    assert completed_data["items"][0]["id"] == second["id"]

    paginated_response = client.get("/tasks", params={"limit": 1, "offset": 1})
    assert paginated_response.status_code == 200
    page_data = paginated_response.json()
    assert page_data["total"] == 3
    assert page_data["limit"] == 1
    assert page_data["offset"] == 1
    assert len(page_data["items"]) == 1
    assert page_data["items"][0]["id"] != first["id"]
