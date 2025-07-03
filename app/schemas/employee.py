# from pydantic import BaseModel, EmailStr
# from datetime import date
# from typing import Optional

# class EmployeeBase(BaseModel):
#     first_name: str
#     last_name: str
#     email: EmailStr
#     phone_number: Optional[str] = None
#     hire_date: date
#     job_title: str
#     salary: float
#     department_id: int

# class EmployeeCreate(EmployeeBase):
#     pass

# class Employee(EmployeeBase):
#     id: int
    
#     class Config:
#         orm_mode = True



from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    hire_date: date
    job_title: str
    salary: float
    department_id: int

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int
    
    class Config:
        from_attributes = True  # Previously called orm_mode in Pydantic v1