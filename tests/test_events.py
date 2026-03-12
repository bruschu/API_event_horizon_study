def test_create_event(override_db, client, auth_headers):
    # Print all registered paths
    for route in client.app.routes:
        if hasattr(route, "path"):
            print(f"DEBUG ROUTE: {route.path}")
    response = client.post(
        "/event/",
        json={
            "name": "Event 1",
            "date": "2026-03-11T11:39:24.683Z",
            "location": "New York City",
        },
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Event 1"
    assert "id" in data


def test_create_event_missing_location(override_db, client, auth_headers):
    response = client.post(
        "/event/",
        json={
            "name": "Incomplet Event",
            "date": "2026-03-11T14:00:00Z",
        },
        headers=auth_headers,
    )

    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["loc"] == ["body", "location"]
    assert data["detail"][0]["msg"] == "Field required"


def test_create_event_invalid_name_type(override_db, client, auth_headers):
    response = client.post(
        "/event/",
        json={
            "name": 123,
            "date": "2026-03-11T14:00:00Z",
            "location": "London",
        },
        headers=auth_headers,
    )

    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["loc"] == ["body", "name"]
    assert "string" in data["detail"][0]["msg"]
