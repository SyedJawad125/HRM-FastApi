# from pydantic import BaseModel
# from typing import Optional

# class DepartmentBase(BaseModel):
#     name: str
#     location: Optional[str] = None

# class DepartmentCreate(DepartmentBase):
#     class Config:
#         extra = "forbid"  # Prevent extra fields in creation

# class Department(DepartmentBase):
#     id: int
#     created_by_user_id: int  # ✅ Required for response schema

#     class Config:
#         from_attributes = True  # For Pydantic v2 (orm_mode=True for v1)


from typing import Optional, List
from pydantic import BaseModel

# (Already defined)
class DepartmentBase(BaseModel):
    name: str
    location: Optional[str] = None

class DepartmentCreate(DepartmentBase):
    class Config:
        extra = "forbid"

class Department(DepartmentBase):
    id: int
    created_by_user_id: int

    class Config:
        from_attributes = True

# ✅ Add this for paginated data
class PaginatedDepartments(BaseModel):
    count: int
    data: List[Department]

# ✅ Add this for final API response
class DepartmentListResponse(BaseModel):
    status: str
    result: PaginatedDepartments
