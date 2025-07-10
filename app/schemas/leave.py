from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum

class LeaveStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class LeaveType(str, Enum):
    ANNUAL = "annual"
    SICK = "sick"
    MATERNITY = "maternity"
    PATERNITY = "paternity"
    UNPAID = "unpaid"
    OTHER = "other"

class LeaveBase(BaseModel):
    start_date: datetime
    end_date: datetime
    leave_type: LeaveType
    reason: str

class LeaveCreate(LeaveBase):
    pass

class LeaveUpdate(BaseModel):
    status: LeaveStatus
    approved_by_id: Optional[int] = None

class LeaveResponse(LeaveBase):
    id: int
    status: LeaveStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    employee_id: int
    approved_by_id: Optional[int] = None

    class Config:
        from_attributes = True

class LeaveList(BaseModel):
    id: int
    start_date: datetime
    end_date: datetime
    leave_type: LeaveType
    status: LeaveStatus
    employee_id: int

    class Config:
        from_attributes = True 

class LeaveListResponse(BaseModel):
    count: int
    data: list[LeaveList]