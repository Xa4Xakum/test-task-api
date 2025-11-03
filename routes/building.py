from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List

from database.init import DataBase, get_database
from .schemas import building

r = APIRouter()


@r.post(
    "/",
    response_model=building.Response,
    status_code=status.HTTP_201_CREATED
)
async def create_building(
    building_data: building.Create,
    db: DataBase = Depends(get_database)
):
    '''
    Добавление нового здания в базу данных
    :return: Созданное здание
    '''
    
    # Проверяем, нет ли уже здания с таким адресом
    existing_building = await db.building.by_address(building_data.address)
    if existing_building:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Building with this address already exists"
        )
    
    new_building = await db.building.add(
        address=building_data.address,
        latitude=building_data.latitude,
        longitude=building_data.longitude,
    )
    
    return new_building


@r.get("/", response_model=List[building.Response])
async def get_all_buildings(
    offset: int | None = None,
    limit: int | None = None,
    db: DataBase = Depends(get_database)
):
    '''
    Получение списка зданий</br>
    Если не задать <bold>limit</bold> и <bold>offset</bold> - 
    вернет список всех зданий
    '''
    return await db.building.get_all(limit=limit, offset=offset)


@r.get("/by-address", response_model=building.Response)
async def bet_buildings_by_address(
    address: str,
    db: DataBase = Depends(get_database)
):
    '''
    Поиск зданий по адресу
    '''
    return await db.building.by_address(address)


@r.get("/in-radius", response_model=List[building.Response])
async def get_in_radius(
    lattitude: float,
    longitude: float,
    radius: float,
    db: DataBase = Depends(get_database)
):
    '''
    Получение всех зданий в радиусе, отсортировано по удаленности</br>
    radius указывается в километрах
    '''
    buildings = await db.building.get_in_radius(lattitude, longitude, radius)
    if len(buildings) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Building not found"
        )
    return buildings


@r.get("/{building_id}/organizations", response_model=List[building.OrganizationResponse])
async def get_building_organizations(
    building_id: int,
    db: DataBase = Depends(get_database)
):
    '''
    Получение всех организаций в конкретном здании
    '''
    building_obj = await db.building.by_id(building_id)
    if not building_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Building not found"
        )
    return building_obj.organizations


@r.get("/{building_id}/with-organizations", response_model=building.WithOrganizationsResponse)
async def get_building_with_organizations(
    building_id: int,
    db: DataBase = Depends(get_database)
):
    '''
    Получение здания со всеми организациями и их данными
    '''
    building_obj = await db.building.by_id(building_id)
    if not building_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Building not found"
        )
    
    return building_obj


@r.get("/{building_id}", response_model=building.Response)
async def get_building(
    building_id: int,
    db: DataBase = Depends(get_database)
):
    '''
    Получение здания по ID
    '''
    building_obj = await db.building.by_id(building_id)
    if not building_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Building not found"
        )
    
    return building_obj
