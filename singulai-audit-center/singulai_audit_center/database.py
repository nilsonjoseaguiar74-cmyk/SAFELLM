from __future__ import annotations

import os
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = os.environ.get(
"DATABASE_URL",
"postgresql+asyncpg://audit_user:audit_pass@localhost:5432/singulai_audit_db",
)

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False)

async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
bind=engine,
expire_on_commit=False,
)

async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session() as session:
        yield session
