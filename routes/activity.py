from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List

from database.init import DataBase, get_database
from .schemas import activity

r = APIRouter()


@r.post(
    "/",
    response_model=activity.Response,
    status_code=status.HTTP_201_CREATED
)
async def create_activity(
    activity_data: activity.Create,
    db: DataBase = Depends(get_database)
):
    '''
    Создание нового вида деятельности
    '''
    existing_activity = await db.activity.by_name(activity_data.name)
    if existing_activity and existing_activity.name == activity_data.name and existing_activity.parent_id == activity_data.parent_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Activity with this name and parent already exists"
        )
    
    # Проверяем вложенность до 3 уровней
    if activity_data.parent_id:
        parent_activity = await db.activity.by_id(activity_data.parent_id)
        if not parent_activity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Parent activity not found"
            )
        
        # Проверяем уровень вложенности родителя
        parent_level = await db.activity.get_nesting_level(activity_data.parent_id)
        if parent_level >= 2:  # Если родитель уже на 2 уровне, новый будет на 3 - максимальный
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Maximum nesting level (3) exceeded"
            )
    
    new_activity = await db.activity.add(
        name=activity_data.name,
        parent_id=activity_data.parent_id,
    )
    return new_activity


@r.get("/", response_model=List[activity.Response])
async def get_all_activities(
    offset: int | None = None,
    limit: int | None = None,
    db: DataBase = Depends(get_database)
):
    '''
    Получение списка деятельности</br>
    Если не задать <bold>limit</bold> и <bold>offset</bold> - 
    вернет список всех активностей
    '''
    return await db.activity.get_all(limit=limit, offset=offset)


@r.get("/tree", response_model=List[activity.TreeResponse])
async def get_activities_tree(
    db: DataBase = Depends(get_database)
):
    '''
    Получение дерева видов деятельности
    '''
    return await db.activity.get_tree()


@r.get("/by-name", response_model=List[activity.Response])
async def search_activities_by_name(
    name_query: str,
    db: DataBase = Depends(get_database)
):
    '''
    Поиск видов деятельности по названию или его части
    '''
    return await db.activity.get_by_name(name_query)


@r.get("/{activity_id}", response_model=activity.Response)
async def get_activity(
    activity_id: int,
    db: DataBase = Depends(get_database)
):
    '''
    Получение вида деятельности по ID
    '''
    activity_obj = await db.activity.by_id(activity_id)
    if not activity_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    return activity_obj