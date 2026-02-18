# Task Manager API

A FastAPI-based Task Management API with CRUD operations, tag support, filtering, pagination, validation, structured errors, tests, and Dockerized runtime.

## Stack
- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL (runtime via Docker Compose)
- SQLite (tests only)
- pytest + httpx

## Features
- `POST /tasks` to create tasks
- `GET /tasks` with filters and pagination:
  - `completed` (boolean)
  - `priority` (1-5)
  - `tags` (CSV any-match)
  - `limit`, `offset`
- `GET /tasks/{id}`
- `PATCH /tasks/{id}` for partial updates
- `DELETE /tasks/{id}` (soft delete)
- Structured error responses
- FastAPI OpenAPI docs at `/docs`

## Error Handling
All API errors follow this structure:

```json
{
  "error": "Validation Failed",
  "details": {
    "priority": "Input should be less than or equal to 5"
  }
}
```

## Project Structure
```text
app/
  api/
  core/
  domain/
  infrastructure/
  services/
tests/
Dockerfile
docker-compose.yml
```

## Run With Docker (Recommended)

```bash
docker compose up --build
```

API will be available at:
- `http://localhost:8000`
- Swagger docs: `http://localhost:8000/docs`

## Local Run (Without Docker)

1. Create virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Set `DATABASE_URL` (optional). Default is local SQLite:
```bash
export DATABASE_URL="sqlite:///./task_manager.db"
```

3. Run server:
```bash
uvicorn app.main:app --reload
```

## Run Tests

```bash
pytest
```

## Key Design Decisions

### Layered Architecture
- `api`: HTTP layer and request/response contracts
- `services`: use-case orchestration and business flow
- `domain`: repository contracts and domain rules
- `infrastructure`: SQLAlchemy models and repository implementations
- `core`: shared utilities (config, logging, time provider, error handling)

### Tagging Implementation: Join Table
Used normalized many-to-many tables (`tasks`, `tags`, `task_tags`).

- Better relational integrity with foreign keys
- Easier deduplication of tags
- Portable across DBs
- More explicit query semantics


### Delete Strategy: Soft Delete
`DELETE /tasks/{id}` marks the task as deleted by setting `deleted_at`.

Because :
- It preserves data for audit and recovery use cases
- It Keeps API behaviour simple by excluding deleted tasks from ureads
- And supports future restore workflows without schema redesign

### Indexing
Indexes are applied to frequently filtered fields:
- `tasks.priority`
- `tasks.completed`
- `tasks.due_date`
- `tasks.deleted_at`
- `tags.name` (unique)

## Notes on Database Choice
- PostgreSQL is the primary runtime DB and is configured in `docker-compose.yml`.
- SQLite is used in tests for fast isolated execution.
