from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from core.config import settings

engine = create_async_engine(settings.DB.DB_URL)

async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

