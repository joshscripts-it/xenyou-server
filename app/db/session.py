# app/db/session.py
import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://postgres:123456@localhost:5433/xenyou"
)

# Async engine for FastAPI (recommended approach)
async_engine = create_async_engine(
    DATABASE_URL,
    future=True,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# Async session factory
async_session_maker = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    future=True,
)


async def init_db():
    """Initialize database tables."""
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting async database session in FastAPI routes."""
    async with async_session_maker() as session:
        yield session


# Alias for backward compatibility
get_db = get_async_session


async def create_db_and_tables():
    """Create database tables - use for development/testing only.

    For production, use Alembic migrations: alembic upgrade head
    """
    try:
        await init_db()
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise
