from sqlalchemy.ext.asyncio import AsyncSession


class BaseCRUD():
    '''базовый класс crud-методов'''

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
