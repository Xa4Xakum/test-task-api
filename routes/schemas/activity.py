from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional


class Create(BaseModel):
    """Схема для создания вида деятельности"""
    name: str = Field(..., min_length=1, max_length=100, description="Название вида деятельности")
    parent_id: Optional[int] = Field(None, ge=1, description="ID родительской деятельности")


class Update(BaseModel):
    """Схема для обновления вида деятельности"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Название вида деятельности")
    parent_id: Optional[int] = Field(None, ge=0, description="ID родительской деятельности (0 для корня)")


class Response(BaseModel):
    """Схема для ответа с видом деятельности"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="ID вида деятельности")
    name: str = Field(..., description="Название вида деятельности")
    parent_id: Optional[int] = Field(None, description="ID родительской деятельности")


class TreeResponse(Response):
    """Схема для дерева видов деятельности"""
    children: List['TreeResponse'] = Field(default_factory=list, description="Дочерние виды деятельности")


class WithChildrenResponse(Response):
    """Схема для вида деятельности с дочерними элементами"""
    children: List[Response] = Field(..., description="Дочерние виды деятельности")

