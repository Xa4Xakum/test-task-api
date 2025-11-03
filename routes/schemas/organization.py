from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

from .activity import Response as ActivityResponse


class PhoneNumberResponse(BaseModel):
    """Схема для ответа с телефонным номером"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="ID телефонного номера")
    number: str = Field(..., description="Номер телефона")


class Create(BaseModel):
    """Схема для создания организации"""
    name: str = Field(..., min_length=1, max_length=255, description="Название организации")
    building_id: int = Field(..., ge=1, description="ID здания")
    phone_numbers: Optional[List[str]] = Field(
        default=None, 
        description="Список телефонных номеров"
    )
    activity_ids: Optional[List[int]] = Field(
        default=None, 
        description="Список ID видов деятельности"
    )


class Update(BaseModel):
    """Схема для обновления организации"""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Название организации")
    building_id: Optional[int] = Field(None, ge=1, description="ID здания")
    phone_numbers: Optional[List[str]] = Field(
        None, 
        description="Список телефонных номеров"
    )
    activity_ids: Optional[List[int]] = Field(
        None, 
        description="Список ID видов деятельности"
    )


class Response(BaseModel):
    """Схема для ответа с организацией"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="ID организации")
    name: str = Field(..., description="Название организации")
    building_id: int = Field(..., description="ID здания")
    phone_numbers: List[PhoneNumberResponse] = Field(..., description="Телефонные номера")
    activities: List[ActivityResponse] = Field(..., description="Виды деятельности")


class ShortResponse(BaseModel):
    """Сокращенная схема для ответа с организацией"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="ID организации")
    name: str = Field(..., description="Название организации")
    building_id: int = Field(..., description="ID здания")