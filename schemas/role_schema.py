from pydantic import BaseModel
from typing import Optional
from datetime import datetime



class RoleCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    created_by: Optional[str] = None  # optional, can be filled in controller

class RoleUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    updated_by: Optional[str] = None

class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str]
    updated_by: Optional[str]
    deleted_at: Optional[datetime]
    deleted_by: Optional[str]
    is_active: bool

    class Config:
        orm_mode = True
