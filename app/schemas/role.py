from typing import Optional, List
from pydantic import BaseModel
from schemas.permission import Permission  # Import nested schema

# ✅ Base schema for shared fields
class RoleBase(BaseModel):
    name: str
    description: str
    code: Optional[str] = None

# ✅ For create endpoint
class RoleCreate(RoleBase):
    permission_ids: Optional[List[int]] = []

    class Config:
        extra = "forbid"

# ✅ For update endpoint
class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    code: Optional[str] = None
    permission_ids: Optional[List[int]] = []

    class Config:
        extra = "forbid"

# ✅ For response model
class Role(RoleBase):
    id: int
    permissions: List[Permission] = []

    class Config:
        from_attributes = True

# ✅ For paginated response
class PaginatedRoles(BaseModel):
    count: int
    data: List[Role]

# ✅ Final API response structure
class RoleListResponse(BaseModel):
    status: str
    result: PaginatedRoles
