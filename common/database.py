from typing import Annotated, AsyncGenerator
from fastapi import Depends, logger
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

from common.settings import settings

engine_master_db = create_async_engine(
    settings.DATABASE_URL, 
    echo=settings.DATABASE_ECHO,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=3600,   # Recycle connections after 1 hour
    max_overflow=10      # Allow up to 10 connections beyond pool size
)

session_master_db = async_sessionmaker(
    bind=engine_master_db, 
    autoflush=False, 
    expire_on_commit=False
)
Base = declarative_base(metadata=MetaData(schema=settings.DATABASE_SCHEMA))

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Get a database session for dependency injection.
    
    This function is enhanced with proper connection tracking and error handling.
    
    Yields:
        AsyncSession: SQLAlchemy async session
    """
    async with session_master_db() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            print(f"Database error occurred: {e}")
            raise
        finally:
            await session.close()

DbDependency = Annotated[AsyncSession, Depends(get_db)]
