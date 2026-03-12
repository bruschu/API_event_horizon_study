from app.core.security import get_password_hash, verify_password


def test_verify_password():
    hashed_password = get_password_hash("Test")
    assert verify_password("Test", hashed_password)
