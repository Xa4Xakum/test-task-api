from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from contextlib import asynccontextmanager

from .engine import engine


@asynccontextmanager  # type: ignore
async def get_async_session() -> AsyncSession:  # type: ignore
    '''
    Генератор сессий для использования в FastAPI Dependency Injection
    
    :yield: Асинхронная сессия БД
    '''
    session = AsyncSessionLocal()
    try:
        yield session  # type: ignore
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


def create_session_factory():
    '''
    Фабрика для создания асинхронных сессий
    '''
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )


# Глобальная фабрика сессий
AsyncSessionLocal = create_session_factory()