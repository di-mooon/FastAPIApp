import logging
from typing import AsyncIterator

from sqlalchemy import MetaData
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from config.config import settings

logger = logging.getLogger()

async_engine = create_async_engine(
    url=settings.db_url,
    pool_pre_ping=True,
    echo=settings.show_sql,
)
async_session = async_sessionmaker(bind=async_engine, autoflush=False, future=True)
metadata = MetaData()
Base = declarative_base(metadata=metadata)


async def init_models():
    async with async_engine.begin() as connection:
        # await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)


async def get_db_session() -> AsyncIterator[AsyncSession]:
    try:
        async with async_session.begin() as session:
            yield session
    except SQLAlchemyError as e:
        logger.exception(e)
