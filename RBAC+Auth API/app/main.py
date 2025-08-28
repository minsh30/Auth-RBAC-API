#main.py

from fastapi import FastAPI 
from sqlalchemy import text 
from app.db.session import engine
from app.db.models import Base
from app.api.auth import router as auth_router
from app.api.users import router as user_router

#create the FastAPI application

app = FastAPI(title = "Auth + RBAC API")

@app.on_event("startup")
async def startup():
    """
    Ensures tables exists on startups
    """

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/health")
async def health():
    """Tiny health check endpoint."""
    async with engine.begin() as conn:
        await conn.execute(text("select 1"))
    return {"status" : "ok"}

#Mount the routers so their endpoints appears as /auth/* and  /users/*
app.include_router(auth_router)
app.include_router(user_router)