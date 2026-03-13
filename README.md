🌌 API Event Horizon

API Event Horizon is a high-performance backend system built with FastAPI designed to handle event management, user registration, and attendee tracking. This project was developed as a deep-dive study into modern backend architecture, containerization, and automated testing pipelines.

🚀 Key Features

Robust Event Management: Complete CRUD operations for creating, updating, and managing event data.

Secure Authentication: User registration and login powered by OAuth2 and JWT (JSON Web Tokens).

Data Integrity: Password hashing using Bcrypt to ensure user security.

Automated Testing: Comprehensive test suite with Pytest, covering authentication and endpoint logic.

Production-Ready CI/CD: Integrated GitHub Actions pipeline that builds a Docker image and runs tests against a live MySQL service container.

🛠 Tech Stack

Backend: FastAPI, Python 3.13

Database: MySQL, SQLAlchemy (ORM)

Security: Bcrypt, JWT

DevOps: Docker, Docker Compose, GitHub Actions

Testing: Pytest

📦 Getting Started

Prerequisites

Docker & Docker Compose

Python 3.13 (optional, if running locally)

Local Setup (with Docker)

Clone the repository:

Bash
git clone https://github.com/bruschu/API_event_horizon_study.git
cd API_event_horizon_study


Build and run the containers:

Bash
docker-compose up --build
Access the interactive API documentation:


Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

🧪 Testing

The project uses pytest for automated testing. In the CI environment, tests are executed inside a Docker container to ensure environment parity.

To run tests locally:

Bash
docker exec -it <container_id> pytest


⚙️ CI/CD Pipeline

The repository includes a GitHub Actions workflow (tests.yml) that:

Spins up a MySQL 8.0 service.

Builds the application's Docker Image.

Injects sensitive configuration via GitHub Secrets.

Runs the full test suite in an isolated environment.


🧠 Technical Challenges & Solutions

1. Environment Parity in CI/CD

Challenge: Tests were passing locally but failing in GitHub Actions due to missing dependencies and database connection issues.
Solution: I transitioned the testing workflow to run entirely inside a Docker container using the python:3.13-slim image. This ensured the CI environment was an exact clone of my local development setup.

2. Database State Isolation

Challenge: Concurrent tests were failing because they tried to create the same "Test User," leading to IntegrityError (Duplicate Entry).
Solution: I implemented a Pytest fixture that utilizes SQLAlchemy's session.rollback(). This ensures that every test runs within a transaction that is reverted at the end, providing a "clean slate" for every single test case.

3. Secure Authentication Logic

Challenge: Encountered ValueError: Invalid salt errors during authentication testing.
Solution: Identified that the test database was being populated with raw strings instead of hashed passwords. I updated the test fixtures to use the Bcrypt hashing utility, ensuring the login logic correctly verifies salted passwords during integration tests.

4. Secret Management

Challenge: Protecting sensitive data like SECRET_KEY and database credentials while keeping the repository public.
Solution: Integrated GitHub Secrets into the CI/CD pipeline. This allowed the application to remain secure while still allowing the automated tests to access necessary environment variables during execution.
