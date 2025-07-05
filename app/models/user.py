from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from app.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from datetime import datetime

from sqlalchemy.orm import relationship

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, nullable=False)
#     email = Column(String, nullable=False, unique=True)
#     password = Column(String, nullable=False)
#     is_active = Column(Boolean, server_default='TRUE', nullable=False)
#     is_admin = Column(Boolean, server_default='FALSE', nullable=False)
#     created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)

#     created_departments = relationship("Department", back_populates="creator")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, server_default='TRUE', nullable=False)
    is_admin = Column(Boolean, server_default='FALSE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)

    # Existing relationship
    created_departments = relationship("Department", back_populates="creator")

    # New relationships
    created_roles = relationship("Role", back_populates="creator")
    created_permissions = relationship("Permission", back_populates="creator")
