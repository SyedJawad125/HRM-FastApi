from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from app.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from datetime import datetime

from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=True)  # ✅ username field
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)  # ✅ renamed for clarity
    is_active = Column(Boolean, server_default='TRUE', nullable=False)
    is_superuser = Column(Boolean, server_default='FALSE', nullable=False)  # ✅ changed to Django-like
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)

    # Existing relationship
    created_departments = relationship("Department", back_populates="creator")

    # New relationships
    created_roles = relationship("Role", back_populates="creator")
    created_permissions = relationship("Permission", back_populates="creator")
