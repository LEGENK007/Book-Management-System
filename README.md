# Intelligent Book Management System

An intelligent, cloud‑ready Book Management API built with **FastAPI**, **async PostgreSQL**, and a locally running **Llama3** model via **Ollama**.  
It supports:

- CRUD for books
- User reviews
- AI‑generated summaries for books and reviews
- JWT authentication with role‑based access control (RBAC)
- Ownership rules (only the admin can update/delete a book)
- Automated tests using pytest

---

## 1. Architecture Overview

**Backend**

- Framework: FastAPI
- Language: Python 3.11+
- Auth: JWT (OAuth2 password flow)
- RBAC: `user` and `admin` roles, plus ownership checks on `Book`

**Database**

- PostgreSQL
- Async access via `sqlalchemy[asyncio]` and `asyncpg`

**AI Integration**

- Local Llama3 model via Ollama HTTP API (`/api/generate`)

**Infrastructure**

- Dockerfile to containerize the FastAPI app
- docker‑compose.yml to orchestrate app + Postgres
- Environment variables (`.env`) to configure DB connection, secrets, and Ollama URL

---

## 2. Prerequisites

To run locally:

- Python **3.11+**
- PostgreSQL 18 (or Docker to run Postgres)
- [Ollama](https://ollama.com) installed and running with the **Llama3** model
- (Optional) Docker & docker‑compose for containerized runs

---

## 3. Run the app locally

**Set environment variables**
- Copy .env.example to .env and set DATABASE_URL, SECRET_KEY, and OLLAMA_URL so the app knows how to connect to Postgres, sign JWTs, and reach Ollama.​

**Start PostgreSQL**
- Run Postgres (either your local installation or a simple postgres Docker container) using the same DB name, user, and password as in DATABASE_URL.​

**Start Ollama with Llama3**
- Install Ollama, pull the llama3 model, and ensure the Ollama service is running at the host/port in OLLAMA_URL so summaries can be generated.​

**Install Python dependencies**
- Create a virtual environment (optional) and run *pip install -r requirements.txt* to install FastAPI, async SQLAlchemy, JWT, and test libraries.​

**Launch the FastAPI server**
- Start the app with *uvicorn app.main:app --reload*, which boots the API, creates tables in the database, and exposes endpoints on http://127.0.0.1:8000.​

**Use the Swagger UI**
- Open http://127.0.0.1:8000/docs to register users, log in to get tokens, and interact with all book, review, and summary endpoints through an interactive web interface.​

---

## 4. Run the app with Docker
**Ensure Docker and Ollama are running**
- ***Docker***: needed for the app and PostgreSQL containers.
- ***Ollama***: must be running on your host with the llama3 model pulled so the container can call it via OLLAMA_URL (typically http://host.docker.internal:11434).​

**Configure environment for Docker**
- In docker-compose.yml, the api service already sets DATABASE_URL, SECRET_KEY, and OLLAMA_URL.
- Adjust these if needed (e.g., change DB credentials or secret key) so the API container can talk to the db service and to Ollama.​

**Build and start the containers**
- From the project root, run: *docker-compose up --build*
- This builds the FastAPI image from the Dockerfile, starts a Postgres container, and then starts the API container linked to that database.​

**Access the API and docs**
- Once containers are up, open:
  1. API root: *http://localhost:8000/*
  2. Swagger UI: *http://localhost:8000/docs*
- Use the docs to register users, log in, and exercise book, review, and recommendation endpoints with the running containers.

**Stop the stack when finished**
- In the same directory, run: *docker-compose down*
- This stops and removes the containers (the Postgres data volume persists unless you remove the volume explicitly).

## Notes & Future Improvements

- Add Alembic migrations for production‑grade schema management.
- Replace Ollama with a cloud LLM endpoint when deploying where local LLM isn’t feasible.
- Add caching for `/recommendations` (e.g., Redis / AWS ElastiCache).
- Extend tests to cover more edge cases and the AI integration with proper mocking.

---