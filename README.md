# 🚀 Auth + RBAC API (FastAPI)

![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?logo=fastapi)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-orange?logo=python)
![JWT](https://img.shields.io/badge/Auth-JWT-blue)
![Status](https://img.shields.io/badge/Status-Completed-green)

A complete **Authentication & Role-Based Access Control (RBAC)** backend built with **FastAPI**, **async SQLAlchemy**, and **JWT**.  

This project demonstrates secure user registration, login with hashed passwords, JWT-based authentication, and protected routes with role-based access (e.g., `admin`, `user`).  

---

## ✨ Features

- 🔐 User registration & login with password hashing (`bcrypt`)
- 🪪 JWT Authentication (access tokens with expiry)
- 👤 Protected routes (`/users/me`) that require a valid token
- 🛡️ Role-based access control (e.g., only `admin` can assign roles)
- 💾 Async database access with SQLAlchemy 2.0 + SQLite (easy to swap for Postgres)
- ⚡ Interactive API docs with Swagger UI at `/docs`
- ✅ Designed with production-ready patterns in mind

---

## 🏗️ Tech Stack

- FastAPI — high-performance Python web framework
- SQLAlchemy 2.0 (async) — ORM for DB models
- SQLite — dev database (can replace with Postgres + `asyncpg`)
- Pydantic v2 — request/response validation
- Passlib — password hashing with bcrypt
- Python-JOSE — JWT signing & verification

---

## ⚙️ Setup & Run Locally

### 1. Clone repository
```
git clone https://github.com/<your-username>/fastapi-auth-rbac.git
cd fastapi-auth-rbac
```

### 2. Create virtual environment
```
python -m venv .venv
# Activate:
# Windows PowerShell
.\.venv\Scripts\Activate
# macOS/Linux
source .venv/bin/activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Run the app
```
uvicorn app.main:app --reload
```

👉 Visit http://127.0.0.1:8000/docs for Swagger UI.

---

## 📌 API Endpoints

### 🔑 Auth
- `POST /auth/register` → Register a new user (default role: `user`)
- `POST /auth/login` → Login, receive JWT access token

### 👥 Users
- `GET /users/me` → Get current logged-in user (requires JWT)
- `POST /users/assign-role` → **Admin-only**: assign a role to another user

### 🩺 Health
- `GET /health` → Simple health check

---

## 🧪 Example Flow

1. **Register**
```
POST /auth/register
{
  "email": "test@example.com",
  "password": "Passw0rd!"
}
```

2. **Login**
```
POST /auth/login
{
  "email": "test@example.com",
  "password": "Passw0rd!"
}
```
Response →  
```
{ "access_token": "....", "token_type": "bearer" }
```

3. **Authorize**  
Add header:  
`Authorization: Bearer <your-token>`

4. **Access protected route**
```
GET /users/me
Response: { "email": "test@example.com" }
```

---

## 🧠 What I Learned

- How FastAPI dependencies (`Depends`) handle auth, DB sessions, and role checks  
- Difference between authentication (who you are) vs authorization (what you can do)  
- How to safely hash & verify passwords with bcrypt  
- How JWTs store identity (`sub`) + expiry (`exp`)  
- How to design SQLAlchemy models with relationships and unique constraints  
- How to implement role-based authorization with reusable dependencies  
- Debugging common FastAPI/SQLAlchemy issues (imports, Pydantic v2, stale reloads)  
- Bootstrapping the first admin user to unlock RBAC-protected routes  

---

## 🚀 Next Steps / Improvements

- 🔄 Add refresh tokens (short-lived access + long-lived refresh)  
- 🛢️ Swap SQLite → Postgres (with `asyncpg`) + Alembic migrations  
- 🧪 Add unit tests (`pytest`, `pytest-asyncio`)  
- 📊 Add structured logging, metrics, and monitoring  
- 🐳 Containerize with Docker + docker-compose  
- 🔐 Add email verification & password reset flows  

---
