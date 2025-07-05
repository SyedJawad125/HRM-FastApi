from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    code = Column(String(50), nullable=False)
    module_name = Column(String(50), nullable=True)

    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="created_permissions")

    roles = relationship("Role", secondary="role_permission", back_populates="permissions")
