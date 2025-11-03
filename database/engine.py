from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

from config.init import conf

from .models import Base


async def create_tables(engine: AsyncEngine):
    '''
    Создание всех таблиц в базе данных
    
    :param engine: Асинхронный движок SQLAlchemy
    '''
    async with engine.begin() as conn:
        # Создаем все таблицы, определенные в моделях
        await conn.run_sync(Base.metadata.create_all)

def create_engine():
    '''
    Создание асинхронного движка PostgreSQL
    '''
    return create_async_engine(
        conf.db_connection,
        echo=False,  # Логировать SQL только в debug режиме
        future=True,
        poolclass=NullPool,  # Для лучшей производительности в async
        pool_pre_ping=True,  # Проверять соединение перед использованием
    )

# Глобальный движок
engine = create_engine()