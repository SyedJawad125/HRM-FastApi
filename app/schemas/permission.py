from pydantic import BaseModel
from typing import Optional

class PermissionBase(BaseModel):
    name: str
    description: str
    code: str
    module_name: Optional[str] = None

class PermissionCreate(PermissionBase):
    pass

class Permission(PermissionBase):
    id: int

    class Config:
        from_attributes = True
