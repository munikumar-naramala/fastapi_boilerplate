from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.db.base import Base


class UserRole(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    role_type = Column(String(32), unique=True, primary_key=True)
    role_description = Column(String(128), nullable=False)
