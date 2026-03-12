from app.core.security import verify_password
from app.model.user import User


def test_create_user(client, db_session, override_db):
    user_data = {"email": "test@example.com", "password": "securepassword123"}

    # 1. Delete only the record that is about to use
    existing_user = (
        override_db.query(User).filter(User.email == "test@example.com").first()
    )
    if existing_user:
        override_db.delete(existing_user)
        override_db.commit()

    # 2. Send request
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201

    # 3. Check the response data
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

    # 4. Verify hashing in the database
    user_in_db = (
        override_db.query(User).filter(User.email == "test@example.com").first()
    )
    assert user_in_db is not None
    assert user_in_db.hashed_password != "securepassword123"
    assert verify_password("securepassword123", user_in_db.hashed_password)
