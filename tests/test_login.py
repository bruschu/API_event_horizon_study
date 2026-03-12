def test_login_success(client, db_session, override_db, test_user):
    # 1. Setup: Create a user in the DB first
    # user_data = {"email": "test@example.com", "password": "securepassword123"}
    # client.post("/users/", json=user_data)

    # 2. Perform the login
    login_data = {"username": "test@example.com", "password": "securepassword123"}
    response = client.post("/login", data=login_data)

    # 3. Assertions
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, db_session, override_db, test_user):
    # 1. Setup: Create user
    # user_data = {"email": "test@example.com", "password": "securepassword123"}
    # client.post("/users/", json=user_data)

    # 2. Try to login with wrong password
    login_data = {"username": "test@example.com", "password": "wrongpassword"}
    response = client.post("/login", data=login_data)

    assert response.status_code == 401
