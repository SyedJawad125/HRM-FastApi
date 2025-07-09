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
from .rank import (
    RankBase,
    RankCreate,
    Rank,
    RankUpdate,
    PaginatedRanks,
    RankListResponse
)
from .attendance import (
    AttendanceBase,
    AttendanceCreate,
    Attendance,
    AttendanceUpdate,
    PaginatedAttendances,
    AttendanceListResponse
)
from .timesheet import (
    TimesheetBase,
    TimesheetCreate,
    Timesheet,
    TimesheetUpdate,
    PaginatedTimesheets,
    TimesheetListResponse
)

from .permission import (
    PermissionBase,
    PermissionCreate,
    PermissionUpdate,
    Permission,
    PaginatedPermissions,
    PermissionListResponse
)
from .role import (
    RoleBase,
    RoleCreate,
    RoleUpdate,
    Role,
    PaginatedRoles,
    RoleListResponse
)

# define what will be exported on `from schemas import *`
__all__ = [
    'UserBase', 'UserCreate', 'LoginRequest', 'UserUpdate', 'UserOut',
    'Token', 'TokenData',
    'Employee', 'EmployeeCreate','PaginatedEmployees','EmployeeListResponse','EmployeeUpdate',
    'DepartmentBase', 'DepartmentCreate', 'Department', 'DepartmentUpdate',
    'PaginatedDepartments', 'DepartmentListResponse',
    'RankBase', 'RankCreate', 'Rank', 'RankUpdate', 'PaginatedRanks', 'RankListResponse',
    'AttendanceBase', 'AttendanceCreate', 'Attendance', 'AttendanceUpdate', 'PaginatedAttendances', 'AttendanceListResponse',
    'TimesheetBase', 'TimesheetCreate', 'Timesheet', 'TimesheetUpdate', 'PaginatedTimesheets', 'TimesheetListResponse',
    'PermissionBase', 'PermissionCreate' ,'PermissionUpdate','Permission', 'PaginatedPermissions', 'PermissionListResponse',
    'RoleBase', 'RoleCreate', 'RoleUpdate', 'Role', 'PaginatedRoles', 'RoleListResponse',

]

