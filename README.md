## Phase 1 MLOPS Roadmap Status

Completed:

- FastAPI
- REST APIs
- PostgreSQL
- SQLAlchemy
- JWT authentication
- Password hashing
- Protected routes
- RBAC admin/user
- Swagger docs
- Environment variables
- Basic logging
- Docker
- Docker Compose
- Pytest tests
- Git/GitHub cleanup


# Enterprise Identity API

A secure FastAPI backend foundation for authentication, authorization, and future AI/MLOps services.

This project implements a production-style backend starter with PostgreSQL, SQLAlchemy, JWT authentication, role-based access control, Docker Compose, logging, environment variables, and automated tests.

---


## Features

- FastAPI REST API
- PostgreSQL database
- SQLAlchemy ORM
- User registration and login
- Password hashing with bcrypt
- JWT access tokens
- Protected routes
- Role-based access control: `user` / `admin`
- Swagger/OpenAPI documentation
- Environment-based configuration
- Docker Compose setup
- Application logging
- Pytest test suite

---

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- bcrypt
- python-jose
- Docker
- Docker Compose
- pytest

---

## Project Structure

```txt
enterprise-identity-api/
│
├── api/                # API routers: auth, admin, health
├── core/               # configuration, database, logging
├── models/             # SQLAlchemy database models
├── schemas/            # Pydantic request/response schemas
├── security/           # password hashing and JWT logic
├── scripts/            # helper scripts
├── tests/              # pytest tests
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
├── .env.example
└── main.py
```

---

## Environment Variables

Create a `.env` file based on `.env.example`.

```env
PROJECT_NAME=Enterprise Identity API
APP_ENV=development

DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/identity_db

SECRET_KEY=replace-me
ACCESS_TOKEN_EXPIRE_MINUTES=15
```

`.env` is private and must not be committed.  
`.env.example` is safe to commit as a template.

---

## Run Locally

Activate the virtual environment:

```powershell
venv\Scripts\activate
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run the API:

```powershell
python -m uvicorn main:app --reload
```

Open Swagger docs:

```txt
http://127.0.0.1:8000/docs
```

---

## Run with Docker Compose

Build and start the full stack:

```powershell
docker compose up --build
```

This starts:

- FastAPI API container
- PostgreSQL database container

Open Swagger docs:

```txt
http://127.0.0.1:8000/docs
```

Stop the stack:

```powershell
docker compose down
```

---

## Main Endpoints

```txt
GET  /health          Health check
POST /auth/register   Register a new user
POST /auth/login      Login with JSON body
POST /auth/token      OAuth2 login for Swagger Authorize
GET  /auth/me         Get current authenticated user
GET  /admin/users     Admin-only users list
```

`/auth/me` requires a valid JWT access token.

`/admin/users` requires an authenticated user with role:

```txt
admin
```

---

## Authentication Flow

```txt
Register
→ validate request
→ hash password with bcrypt
→ save user in PostgreSQL

Login
→ verify email and password
→ generate JWT access token

Protected route
→ read Bearer token
→ decode and validate JWT
→ fetch user from database
→ return current user
```

---

## Authorization Flow

```txt
Authenticated user
→ load current user from JWT
→ check user role
→ allow or reject access
```

Example:

```txt
role = user   → cannot access /admin/users
role = admin  → can access /admin/users
```

---

## Testing

Run tests:

```powershell
pytest -v
```

Current tests cover:

- health check endpoint
- user registration
- user login
- JWT token generation
- protected route access
- protected route rejection without token

Expected result:

```txt
3 passed
```

---

## Security Notes

This project avoids committing sensitive or local runtime files:

- `.env`
- logs
- virtual environments
- private/public key files
- Python cache files

Secrets must be provided through environment variables.

---
