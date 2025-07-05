from .user import User
from .employee import Employee
from .department import Department
from .permission import Permission
from .role import Role, role_permission  # bring role_permission here
from .association_tables import user_role  # bring user_role from new file

__all__ = [
    "User", "Employee", "Department", "Permission",
    "Role", "role_permission", "user_role"
]
