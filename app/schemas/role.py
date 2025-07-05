from pydantic import BaseModel
from typing import Optional, List
from schemas.permission import Permission  # Import the Permission schema

class RoleBase(BaseModel):
    name: str
    description: str
    code: Optional[str] = None

class RoleCreate(RoleBase):
    permission_ids: Optional[List[int]] = []

class Role(RoleBase):
    id: int
    permissions: List[Permission] = []

    class Config:
        from_attributes = True
