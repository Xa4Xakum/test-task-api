from pydantic import BaseModel, ConfigDict
from typing import List, Optional

from .organization import Response as OrganizationResponse

class Create(BaseModel):
    address: str
    latitude: float
    longitude: float

class Update(BaseModel):
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class Response(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    address: str
    latitude: float
    longitude: float

class WithOrganizationsResponse(Response):
    organizations: List[OrganizationResponse]
