# Enterprise Identity API

A secure FastAPI backend foundation for authentication, authorization, and future AI/MLOps services.

This project is part of a backend and MLOps learning roadmap. It provides a production-style API foundation with PostgreSQL, JWT authentication, role-based access control, Docker Compose, logging, environment variables, and automated tests.

---

## Features

- FastAPI backend
- REST API structure
- PostgreSQL database
- SQLAlchemy ORM
- User registration
- User login
- Password hashing with bcrypt
- JWT access tokens
- Protected routes
- Role-based access control
  - `user`
  - `admin`
- Swagger/OpenAPI documentation
- Environment variables with `.env`
- Docker Compose setup
- Basic application logging
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
├── api/                # API routers and endpoints
├── core/               # Config, database, logging
├── models/             # SQLAlchemy models
├── schemas/            # Pydantic request/response schemas
├── security/           # Password hashing and JWT logic
├── scripts/            # Helper scripts
├── tests/              # Pytest tests
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
├── .env.example
└── main.py