from datetime import date, timedelta


def future_date(days: int = 3) -> str:
    return (date.today() + timedelta(days=days)).isoformat()


def create_task(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Delete target",
            "priority": 3,
            "due_date": future_date(),
            "tags": ["cleanup"],
        },
    )
    assert response.status_code == 201
    return response.json()


def test_soft_delete_hides_task_from_get_and_list(client):
    created = create_task(client)

    delete_response = client.delete(f"/tasks/{created['id']}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/tasks/{created['id']}")
    assert get_response.status_code == 404

    list_response = client.get("/tasks")
    assert list_response.status_code == 200
    data = list_response.json()
    assert data["total"] == 0
    assert data["items"] == []


def test_soft_delete_is_not_idempotent_for_missing_active_task(client):
    created = create_task(client)

    first_delete = client.delete(f"/tasks/{created['id']}")
    assert first_delete.status_code == 204

    second_delete = client.delete(f"/tasks/{created['id']}")
    assert second_delete.status_code == 404
