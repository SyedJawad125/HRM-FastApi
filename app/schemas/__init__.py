# user schemas
from .user import (
    UserBase,
    UserCreate,
    LoginRequest,
    UserUpdate,
    UserOut,
    Token,
    TokenData
)

# employee schemas
from .employee import (
    Employee,
    EmployeeCreate,
    PaginatedEmployees,
    EmployeeListResponse,
    EmployeeUpdate
)

# department schemas
from .department import (
    DepartmentBase,
    DepartmentCreate,
    Department,
    DepartmentUpdate,
    PaginatedDepartments,
    DepartmentListResponse
)

# define what will be exported on `from schemas import *`
__all__ = [
    'UserBase', 'UserCreate', 'LoginRequest', 'UserUpdate', 'UserOut',
    'Token', 'TokenData',
    'Employee', 'EmployeeCreate','PaginatedEmployees','EmployeeListResponse','EmployeeUpdate',
    'DepartmentBase', 'DepartmentCreate', 'Department', 'DepartmentUpdate',
    'PaginatedDepartments', 'DepartmentListResponse'

]
