from sqlalchemy import inspect, text


def test_database_connection(db_session):
    result = db_session.execute(text("SELECT 1"))
    assert result is not None


def test_user_table_exists(db_session):
    # 'inspect' looks at the database structure
    inspector = inspect(db_session.bind)
    tables = inspector.get_table_names()
    assert "user" in tables
    assert "event" in tables
    assert "attendee" in tables
