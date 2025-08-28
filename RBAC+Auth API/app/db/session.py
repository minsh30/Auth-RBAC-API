#/db/session.py
#With the help of this file every request gets its own session

#from sqlalchemy.ext.asycio import(AsyncSession, create_async_engine, async_sessionmaker)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from collections.abc import AsyncGenerator
from app.core.config import settings

#Create async engine using URL in .env file
engine = create_async_engine(
    settings.DATABASE_URL,
    future = True,
    echo = False
)

#Factory that creates AsyncSession objects
AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False, #helps in keeping object resuable after commit
    class_ = AsyncSession
)

#FastAPI Dependency:yields a fresh AsyncSession per request

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session



