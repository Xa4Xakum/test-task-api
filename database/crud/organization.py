from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..models import Organization, PhoneNumber, Activity, OrganizationActivity
from .base import BaseCRUD


class Add(BaseCRUD):
    '''Методы добавления организаций'''
    
    async def add(
        self,
        name: str,
        building_id: int,
        phone_numbers: Optional[List[str]] = None,
        activity_ids: Optional[List[int]] = None,
    ) -> Organization:
        '''
        Добавление новой организации в базу данных
        
        :param name: Название организации
        :param building_id: ID здания, где расположена организация
        :param phone_numbers: Список телефонных номеров
        :param activity_ids: Список ID видов деятельности
        :return: Объект созданной организации
        '''
        organization = Organization(
            name=name,
            building_id=building_id,
        )
        self.session.add(organization)
        await self.session.flush()
        
        if phone_numbers:
            for phone_number in phone_numbers:
                phone = PhoneNumber(
                    organization_id=organization.id,
                    number=phone_number
                )
                self.session.add(phone)
        
        if activity_ids:
            for activity_id in activity_ids:
                org_activity = OrganizationActivity(
                    organization_id=organization.id,
                    activity_id=activity_id
                )
                self.session.add(org_activity)
        
        await self.session.commit()
        await self.session.refresh(organization)
        return organization


class Get(BaseCRUD):
    '''Методы получения организаций'''
    
    async def by_id(self, organization_id: int) -> Optional[Organization]:
        '''
        Получение организации по ID
        
        :param organization_id: ID организации
        :return: Объект организации или None если не найден
        '''
        result = await self.session.execute(
            select(Organization)
            .where(Organization.id == organization_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, limit: int | None = None, offset: int | None = None) -> List[Organization]:
        '''
        Получение всех организаций
        
        :return: Список всех организаций
        '''
        query = select(Organization)

        if offset: query = query.offset(offset)
        if limit: query = query.limit(limit)

        query = query.order_by(Organization.name)
        result = await self.session.execute(query)
        return result.scalars().all()  # type: ignore

    async def get_by_building(self, *building_id: int) -> List[Organization]:
        '''
        Получение организаций по зданию
        
        :param building_id: ID здания
        :return: Список организаций в указанном здании
        '''
        result = await self.session.execute(
            select(Organization)
            .where(Organization.building_id.in_(building_id))
            .order_by(Organization.name)
        )
        return result.scalars().all()  # type: ignore
    
    async def get_by_activity(self, activity_id: int) -> List[Organization]:
        '''
        Получение организаций по виду деятельности
        
        :param activity_id: ID вида деятельности
        :return: Список организаций с указанным видом деятельности
        '''
        activity = await self.session.execute(
            select(Activity)
            .where(Activity.id == activity_id)
            .options(
                selectinload(Activity.children, recursion_depth=3)
            )
        )
        ids = self._get_activity_and_children_ids(activity.scalar())
        result = await self.session.execute(
            select(Organization)
            .join(Organization.activities)
            .where(Activity.id.in_(ids))
            .order_by(Organization.name)
            .group_by(Organization.id)
        )
        return result.scalars().all()  # type: ignore

    def _get_activity_and_children_ids(self, activity: Activity) -> List[int]:
        '''Получить список id активности и всех потомков'''
        ids = [activity.id]
        if activity.children:
            for i in activity.children:
                for j in self._get_activity_and_children_ids(i): ids.append(j)
        return ids
    
    async def get_by_name(self, search_term: str) -> List[Organization]:
        '''
        Поиск организаций по названию (регистронезависимый)
        
        :param search_term: Строка для поиска
        :return: Список найденных организаций
        '''
        result = await self.session.execute(
            select(Organization)
            .where(Organization.name.ilike(f"%{search_term}%"))
            .order_by(Organization.name)
        )
        return result.scalars().all()  # type: ignore


class Update(BaseCRUD):
    '''Методы обновления организаций'''


class Delete(BaseCRUD):
    '''Методы удаления организаций'''


class CRUD(Add, Get, Update, Delete):
    '''CRUD для организаций'''
