Phase 1: Local & GitHub Setup

[X] Create a new project folder and open it in VS Code.

[X] Initialize a local Git repository (git init).

[X] Create a .gitignore file (crucial for Python and Docker).

[X] Create a new repository on GitHub and link it to your local folder.

[X] Create a README.md explaining the project.

Phase 2: The Docker "Skeleton"

[ ] Create a requirements.txt (start with fastapi, uvicorn, sqlalchemy, mysql-connector-python).

[ ] Write an optimized Dockerfile (remember the layer order: copy requirements first, then install, then copy code).

[ ] Write a docker-compose.yml with two services: app and db.

[ ] Configure a Docker Volume for the MySQL data to ensure persistence.

[ ] Create a .env file for your database credentials (and don't push it to GitHub!).

Phase 3: Database & Backend Logic

[ ] Set up the SQLAlchemy Base and engine connection.

[ ] Define your Models (Event and Attendee) with their relationships.

[ ] Create a schemas.py (Pydantic models) for data validation.

[ ] Implement CRUD routes (Create, Read, Update, Delete) for Events.

[ ] Create a route to "Register" an attendee to a specific event.

Phase 4: Migrations & Persistence

[ ] Initialize Alembic inside the container.

[ ] Generate your first migration script (revision --autogenerate).

[ ] Run the migration to create the tables in MySQL.

[ ] Test Persistence: Stop containers, docker compose down, bring them up again, and check if the data is still there.

Phase 5: Automation (The "DevOps" Touch)

[ ] Create a tests/ folder and write at least two basic tests using Pytest.

[ ] Set up a GitHub Actions workflow (.github/workflows/main.yml).

[ ] Configure the workflow to:

Build the Docker image.

Run the tests automatically on every push.

[ ] Set up GitHub Secrets for any sensitive data needed during the CI build.