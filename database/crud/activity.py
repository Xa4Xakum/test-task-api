from typing import Optional, List
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from ..models import Activity, Organization
from .base import BaseCRUD


class Add(BaseCRUD):
    '''Методы добавления видов деятельности'''
    
    async def add(
        self,
        name: str,
        parent_id: Optional[int] = None,
    ) -> Activity:
        '''
        Добавление нового вида деятельности в базу данных
        
        :param name: Название вида деятельности
        :param parent_id: ID родительской деятельности
        :return: Объект созданной деятельности
        '''
        activity = Activity(
            name=name,
            parent_id=parent_id,
        )
        self.session.add(activity)
        await self.session.commit()
        await self.session.refresh(activity)
        return activity


class Get(BaseCRUD):
    '''Методы получения видов деятельности'''
    
    async def by_id(self, activity_id: int) -> Optional[Activity]:
        '''
        Получение вида деятельности по ID
        
        :param activity_id: ID вида деятельности
        :return: Объект деятельности или None если не найден
        '''
        result = await self.session.execute(
            select(Activity)
            .where(Activity.id == activity_id)
        )
        return result.scalar_one_or_none()
    
    async def by_list_id(self, activity_ids: List[int]) -> List[Activity]:
        '''
        Получение вида деятельности по ID
        
        :param activity_id: ID вида деятельности
        :return: Объект деятельности или None если не найден
        '''
        result = await self.session.execute(
            select(Activity)
            .where(Activity.id.in_(activity_ids))
            .order_by(Activity.id)
        )
        return result.scalars().all()  # type: ignore
    
    async def by_name(self, name: str) -> Optional[Activity]:
        '''
        Получение вида деятельности по названию
        
        :param name: Название вида деятельности
        :return: Объект деятельности или None если не найден
        '''
        result = await self.session.execute(
            select(Activity)
            .where(Activity.name == name)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self, limit: int | None = None, offset: int | None = None) -> List[Activity]:
        '''
        Получение всех видов деятельности
        
        :return: Список всех видов деятельности
        '''
        query = select(Activity)

        if offset: query = query.offset(offset)
        if limit: query = query.limit(limit)

        query = query.order_by(Activity.name)
        result = await self.session.execute(query)
        return result.scalars().all()  # type: ignore

    async def get_tree(self) -> List[Activity]:
        '''
        Получение дерева видов деятельности
        
        :return: Дерево видов деятельности (только корневые элементы с детьми)
        '''
        result = await self.session.execute(
            select(Activity)
            .where(Activity.parent_id.is_(None))
            .order_by(Activity.name)
        )
        return result.scalars().all()

    async def get_by_name(self, search_term: str) -> List[Activity]:
        '''
        Поиск видов деятельности по названию (регистронезависимый)
        
        :param search_term: Строка для поиска
        :return: Список найденных видов деятельности
        '''
        result = await self.session.execute(
            select(Activity)
            .where(Activity.name.ilike(f"%{search_term}%"))
            .order_by(Activity.name)
        )
        return result.scalars().all()

    async def get_nesting_level(self, activity_id: int, current_level: int = 0) -> int:
        '''
        Получение уровня вложенности вида деятельности
        
        :param activity_id: ID вида деятельности
        :param current_level: Текущий уровень (для рекурсии)
        :return: Уровень вложенности (0 - корень, 1, 2, 3)
        '''
        activity_obj = await self.by_id(activity_id)
        if not activity_obj or not activity_obj.parent_id:
            return current_level
        
        # Рекурсивно поднимаемся по дереву
        return await self.get_nesting_level(activity_obj.parent_id, current_level + 1)


class Update(BaseCRUD):
    '''Методы обновления видов деятельности'''


class Delete(BaseCRUD):
    '''Методы удаления видов деятельности'''


class CRUD(Add, Get, Update, Delete):
    '''CRUD для видов деятельности'''