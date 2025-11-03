import math
from typing import Optional, List, Tuple

from sqlalchemy import select, update, delete, func

from ..models import Building
from .base import BaseCRUD


class Add(BaseCRUD):
    '''Методы добавления зданий'''

    async def add(
        self,
        address: str,
        latitude: float,
        longitude: float,
    ) -> Building:
        '''
        Добавление нового здания в базу данных

        :param address: Адрес здания
        :param latitude: Географическая широта
        :param longitude: Географическая долгота
        :return: Объект созданного здания
        '''
        building = Building(
            address=address,
            latitude=latitude,
            longitude=longitude,
        )
        self.session.add(building)
        await self.session.commit()
        await self.session.refresh(building)
        return building


class Get(BaseCRUD):
    '''Методы получения зданий'''

    async def by_id(self, building_id: int) -> Optional[Building]:
        '''
        Получение здания по ID
        
        :param building_id: ID здания
        :return: Объект здания или None если не найден
        '''
        result = await self.session.execute(
            select(Building)
            .where(Building.id == building_id)
        )
        return result.scalar_one_or_none()

    async def by_address(self, address: str) -> Optional[Building]:
        '''
        Получение здания по адресу
        
        :param address: Адрес здания
        :return: Объект здания или None если не найден
        '''
        result = await self.session.execute(
            select(Building)
            .where(Building.address == address)
        )
        return result.scalar_one_or_none()

    async def get_all(self, limit: int | None = None, offset: int | None = None) -> List[Building]:
        '''
        Получение всех зданий
        
        :return: Список всех зданий
        '''
        query = select(Building)

        if offset: query = query.offset(offset)
        if limit: query = query.limit(limit)

        query = query.order_by(Building.id)
        result = await self.session.execute(query)
        return result.scalars().all()  # type: ignore

    async def get_in_radius(
        self, 
        lat: float, 
        lon: float, 
        radius: float
    ) -> List[Building]:
        '''
        Получение зданий в радиусе без информации о расстоянии
        '''
        distance_expr = self._calculate_distance(lat, lon)
        
        result = await self.session.execute(
            select(Building)
            .where(distance_expr <= radius)
            .order_by(distance_expr)
        )
        
        return result.scalars().all()  # type: ignore

    def _calculate_distance(self, lat: float, lon: float):
        '''
        Вычисление расстояния по формуле гаверсинуса
        '''
        # Константы
        earth_radius = 6371
        
        # Преобразование градусов в радианы
        center_lat = func.radians(lat)
        center_lon = func.radians(lon)
        building_lat = func.radians(Building.latitude)
        building_lon = func.radians(Building.longitude)
        
        # Разницы
        dlat = building_lat - center_lat
        dlon = building_lon - center_lon
        
        # Формула гаверсинуса
        a = (
            func.sin(dlat / 2) * func.sin(dlat / 2) +
            func.cos(center_lat) * func.cos(building_lat) *
            func.sin(dlon / 2) * func.sin(dlon / 2)
        )
        c = 2 * func.atan2(func.sqrt(a), func.sqrt(1 - a))
        distance = earth_radius * c
        
        return distance


class Update(BaseCRUD):
    '''Методы обновления зданий'''


class Delete(BaseCRUD):
    '''Методы удаления зданий'''


class CRUD(Add, Get, Update, Delete):
    '''CRUD для зданий'''
