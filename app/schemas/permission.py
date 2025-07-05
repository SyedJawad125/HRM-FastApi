from typing import Optional, List
from pydantic import BaseModel

# ✅ Base schema for shared fields
class PermissionBase(BaseModel):
    name: str
    description: str
    code: str
    module_name: Optional[str] = None

# ✅ For create endpoint
class PermissionCreate(PermissionBase):
    class Config:
        extra = "forbid"

# ✅ For update endpoint
class PermissionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    code: Optional[str] = None
    module_name: Optional[str] = None

    class Config:
        extra = "forbid"

# ✅ For response model
class Permission(PermissionBase):
    id: int

    class Config:
        from_attributes = True

# ✅ For paginated response
class PaginatedPermissions(BaseModel):
    count: int
    data: List[Permission]

# ✅ Final API response structure
class PermissionListResponse(BaseModel):
    status: str
    result: PaginatedPermissions
