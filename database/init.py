from sqlalchemy.ext.asyncio import AsyncSession

from .crud import building, organization, activity
from .session import get_async_session


class DataBase():
    '''
    Класс для работы с базой данных
    '''

    def __init__(self, session: AsyncSession) -> None:
        pass
        self.building = building.CRUD(session)
        self.organization = organization.CRUD(session)
        self.activity = activity.CRUD(session)


async def get_database() -> DataBase:  # type: ignore
    '''
    Dependency для инъекции фасада базы данных
    '''
    async with get_async_session() as session:
        yield DataBase(session)  # type: ignore
