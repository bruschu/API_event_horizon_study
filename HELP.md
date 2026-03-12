Phase 1: Local & GitHub Setup

[X] Create a new project folder and open it in VS Code.

[X] Initialize a local Git repository (git init).

[X] Create a .gitignore file (crucial for Python and Docker).

[X] Create a new repository on GitHub and link it to your local folder.

[X] Create a README.md explaining the project.

Phase 2: The Docker "Skeleton"

[X] Create a requirements.txt (start with fastapi, uvicorn, sqlalchemy, mysql-connector-python).

[X] Write an optimized Dockerfile (remember the layer order: copy requirements first, then install, then copy code).

[X] Write a docker-compose.yml with two services: app and db.

[X] Configure a Docker Volume for the MySQL data to ensure persistence.

[X] Create a .env file for your database credentials (and don't push it to GitHub!).

Phase 3: Database & Backend Logic

[X] Set up the SQLAlchemy Base and engine connection.

[X] Define your Models (Event and Attendee) with their relationships.

[X] Create a schemas.py (Pydantic models) for data validation.

[X] Implement CRUD routes (Create, Read, Update, Delete) for Events.

[X] Create a route to "Register" an attendee to a specific event.

Phase 4: Migrations & Persistence

[X] Initialize Alembic inside the container.

[X] Generate your first migration script (revision --autogenerate).

[X] Run the migration to create the tables in MySQL.

[X] Test Persistence: Stop containers, docker compose down, bring them up again, and check if the data is still there.

Phase 5: Automation (The "DevOps" Touch)

[X] Create a tests/ folder and write at least two basic tests using Pytest.

[ ] Set up a GitHub Actions workflow (.github/workflows/main.yml).

[ ] Configure the workflow to:

Build the Docker image.

Run the tests automatically on every push.

[ ] Set up GitHub Secrets for any sensitive data needed during the CI build.

---

Create the Virtual Environment:
python3 -m venv .venv

Activate it:
source .venv/bin/activate

Upgrade Pip and Install Base Libraries:
pip install --upgrade pip
pip install fastapi uvicorn sqlalchemy mysql-connector-python

Create your initial requirements.txt:
pip freeze > requirements.txt

---

Run Uvicorn
uvicorn app.main:app --reload

---

Docker

Building and Starting -> docker compose up --build
Checking the Status -> docker compose ps
Reading the Logs -> docker compose logs -f app
Stopping and Cleaning Up -> Stopping and Cleaning Up
Test with pytest -> docker compose exec api pytest


---

Alembic

Initialization -> docker compose exec api alembic init alembic
Autogenerate (Every time you change models.py) -> docker compose exec api alembic revision --autogenerate -m "Description of change"
Upgrade -> docker compose exec api alembic upgrade head
