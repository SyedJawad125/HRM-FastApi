# from .user import LoginRequest, Token
# from .user import (
#     UserBase,
#     UserCreate,
#     LoginRequest,  # Make sure this is included
#     UserUpdate,
#     UserOut,
#     Token,
#     TokenData
# )
# from .employee import Employee, EmployeeCreate
# from .department import Department, DepartmentCreate
# from .user import UserOut, UserCreate, UserUpdate, Token, TokenData
# from .user import LoginRequest, Token
# __all__ = [
#     'UserBase', 'UserCreate', 'LoginRequest', 'UserUpdate', 'UserOut',
#     'Token', 'TokenData',
#     'Employee', 'EmployeeCreate',
#     'Department', 'DepartmentCreate'
# ]

# from .department import (
#     DepartmentBase,
#     DepartmentCreate,
#     Department,
#     PaginatedDepartments,
#     DepartmentListResponse,
#     DepartmentUpdate
# )

# __all__ = [
#     'DepartmentBase',
#     'DepartmentCreate',
#     'Department',
#     'PaginatedDepartments',
#     'DepartmentListResponse',
#     'DepartmentUpdate'
# ]




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
    EmployeeCreate
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
    'Employee', 'EmployeeCreate',
    'DepartmentBase', 'DepartmentCreate', 'Department', 'DepartmentUpdate',
    'PaginatedDepartments', 'DepartmentListResponse'
]
