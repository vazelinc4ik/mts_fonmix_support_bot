
from typing import List, Optional, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession

from core import async_session_maker
from models import Stores, TVDetails


ModelType = TypeVar("ModelType", bound=DeclarativeBase)

class BaseCRUD:
    model: Type[DeclarativeBase] = None
    
    @classmethod
    async def find_one_or_none(cls, **filter_by) -> Optional[ModelType]:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.unique().scalar_one_or_none()
    
    @classmethod
    async def find_all(cls, **filter_by) -> List[ModelType]:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()
    
class StoresCRUD(BaseCRUD):
    model = Stores
    
class TVDetailsCRUD(BaseCRUD):
    model = TVDetails
    
    @classmethod
    async def find_all_names_by_store_id(cls, store_id: int) -> List[str]:
        async with async_session_maker() as session:
            query = select(cls.model.name).filter_by(store_id=store_id)
            result = await session.execute(query)
            return result.scalars().all()
        