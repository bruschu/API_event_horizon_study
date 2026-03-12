import pytest
from fastapi.testclient import TestClient

from app.core.database import get_db
from app.core.security import create_access_token
from app.main import app
from app.model.user import User


@pytest.fixture
def db_session():
    # 1. Setup: get the session
    db_generator = get_db()
    session = next(db_generator)
    session.begin()

    # 2. Provide the session to the test
    yield session

    # 3. Teardown: close the session after the test finishes
    session.rollback()
    session.close()


@pytest.fixture
def override_db(db_session):
    # 1. Setup: Define the override
    def override_get_db():
        yield db_session

    # 2. Apply the override
    app.dependency_overrides[get_db] = override_get_db

    yield db_session

    # 3. Teardown: Clear the override
    app.dependency_overrides.clear()


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def auth_headers():
    access_token = create_access_token(data={"sub": "test@example.com"})
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def test_user(db_session):
    # Create the user that matches the 'sub' in your auth_headers
    user = User(email="test@example.com", password="hashed_password")
    db_session.add(user)
    db_session.commit()
    return user
