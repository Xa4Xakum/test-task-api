from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from database.init import DataBase, get_database
from .schemas import organization

r = APIRouter()


@r.post(
    "/",
    response_model=organization.Response,
    status_code=status.HTTP_201_CREATED
)
async def create_organization(
    organization_data: organization.Create,
    db: DataBase = Depends(get_database)
):
    '''
    Добавление новой организации в базу данных
    :return: Созданная организация
    '''
    
    building = await db.building.by_id(organization_data.building_id)
    if not building:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Building not found"
        )
    
    existing_organization = await db.organization.get_by_name(organization_data.name)
    if existing_organization:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization with this name already exists"
        )
    
    ids = organization_data.activity_ids
    if ids:
        checked = []
        in_db = [i.id for i in await db.activity.by_list_id(ids)]

        for i in ids:
            if i in checked: raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Duplicate activity id"
            )
            if i not in in_db: raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Activity {i} not found"
            )
            checked.append(i)
            

    new_organization = await db.organization.add(
        name=organization_data.name,
        building_id=organization_data.building_id,
        phone_numbers=organization_data.phone_numbers,
        activity_ids=organization_data.activity_ids,
    )
    
    return new_organization


@r.get("/", response_model=List[organization.Response])
async def get_all_organizations(
    offset: int | None = None,
    limit: int | None = None,
    db: DataBase = Depends(get_database)
):
    '''
    Получение списка организаций</br>
    Если не задать <bold>limit</bold> и <bold>offset</bold> - 
    вернет список всех организаций
    '''
    return await db.organization.get_all(limit=limit, offset=offset)


@r.get("/by-name", response_model=List[organization.Response])
async def get_organizations_by_name(
    name: str,
    db: DataBase = Depends(get_database)
):
    '''
    Поиск организаций по названию или его части
    '''
    return await db.organization.get_by_name(name)


@r.get("/in-radius", response_model=List[organization.Response])
async def get_in_radius(
    lattitude: float,
    longitude: float,
    radius: float,
    db: DataBase = Depends(get_database)
):
    '''
    Получение всех организаций в радиусе, отсортировано по удаленности</br>
    radius указывается в километрах
    '''
    buildings = await db.building.get_in_radius(lattitude, longitude, radius)
    organizations = await db.organization.get_by_building(*[i.id for i in buildings])
    if len(organizations) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Building not found"
        )
    return organizations


@r.get("/{organization_id}", response_model=organization.Response)
async def get_organization(
    organization_id: int,
    db: DataBase = Depends(get_database)
):
    '''
    Получение организации по ID
    '''
    organization_obj = await db.organization.by_id(organization_id)
    if not organization_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    return organization_obj


@r.get("/activity/{activity_id}", response_model=List[organization.Response])
async def get_organizations_by_activity(
    activity_id: int,
    db: DataBase = Depends(get_database)
):
    '''
    Получение организаций по виду деятельности
    '''
    return await db.organization.get_by_activity(activity_id)
