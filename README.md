# 🚀 Auth + RBAC API (FastAPI)

A demo **Authentication & Role-Based Access Control (RBAC)** backend built with **FastAPI**, **SQLAlchemy (async)**, and **JWT**.

This project shows how to implement secure user management, login with hashed passwords, and protect routes with role-based access (e.g., `admin`, `user`).  
It’s designed as a learning project but follows patterns close to production-ready systems.

---

## ✨ Features

- 🔐 **User registration & login** with password hashing (bcrypt)
- 🪪 **JWT Authentication** (access tokens with expiry)
- 👤 **Protected routes** (`/users/me`) that require a valid token
- 🛡️ **Role-based access control** (e.g., only `admin` can assign roles)
- 💾 **Async database access** with SQLAlchemy 2.0 + SQLite (easy to swap to Postgres)
- ⚡ Built with **FastAPI** → interactive API docs at `/docs`
- ✅ Unit-test ready (with `pytest`)

---

## 🏗️ Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) — modern Python web framework
- [SQLAlchemy (async)](https://docs.sqlalchemy.org/en/20/) — ORM for DB models
- [SQLite](https://www.sqlite.org/index.html) — dev database (swap to Postgres in production)
- [Pydantic v2](https://docs.pydantic.dev/) — request/response validation
- [Passlib](https://passlib.readthedocs.io/en/stable/) — password hashing
- [Python-JOSE](https://python-jose.readthedocs.io/en/latest/) — JWT signing/verification

---

## ⚙️ Setup & Run Locally

### 1. Clone repo
```bash
git clone https://github.com/<your-username>/fastapi-auth-rbac.git
cd fastapi-auth-rbac


### 2. Create virtual environment

python -m venv .venv

# Activate it:
# Windows PowerShell
.\.venv\Scripts\Activate

# macOS/Linux
source .venv/bin/activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Run the app
uvicorn app.main:app --reload


Visit 👉 http://127.0.0.1:8000/docs
 for Swagger UI.


## 📌 API Endpoints
Auth

    - POST /auth/register → Register a new user (default role: user)

    - POST /auth/login → Login, receive JWT access token

Users

    - GET /users/me → Get current logged-in user (requires JWT)

    - POST /users/assign-role → Admin-only: assign role to a user

Health

    - GET /health → Simple healthcheck

🧪 Example Flow

Register:

    - POST /auth/register
{ "email": "test@example.com", "password": "Passw0rd!" }


Login:

    - POST /auth/login
        { "email": "test@example.com", "password": "Passw0rd!" }


        Response → { "access_token": "....", "token_type": "bearer" }

        Authorize → Add header:
        Authorization: Bearer <your-token>

        Access protected route:

    - GET /users/me
        { "email": "test@example.com" }

## 🧠 What I Learned

Building this project helped me learn:

 - How FastAPI dependencies (Depends) can be used for DB sessions, auth, and role checks

- The difference between authentication (who you are) vs authorization (what you can do)

- How to safely hash & verify passwords with bcrypt

- How JWTs store identity (sub) + expiry (exp)

- How to design SQLAlchemy models with relationships and constraints

- How to build protected routes with reusable dependencies like current_user and require_role

- How to debug common issues (wrong types in mapped_column, stale reloads, missing packages like email-validator)

- How to bootstrap the first admin user for RBAC systems

## 🚀 Next Steps (Improvements)

🔄 Add refresh tokens (short-lived access + long-lived refresh)

🛢️ Swap SQLite for Postgres (with asyncpg) + Alembic migrations

🧑‍💻 Add unit tests with pytest-asyncio

📊 Add logging, monitoring, and metrics

🐳 Containerize with Docker + docker-compose

🔐 Add email verification & password reset flows

## 📚 References

    - FastAPI Docs

    - SQLAlchemy 2.0 ORM

    - Passlib bcrypt

    - JWT RFC
