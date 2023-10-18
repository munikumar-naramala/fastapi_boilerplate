from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from app.db.base import Base
from app.models.user_role import UserRole


class User(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_name = Column(String(128), unique=True, primary_key=True)
    email = Column(String(128), unique=True, primary_key=True)
    password = Column(String(256))
    mobile = Column(String(15), unique=True, primary_key=True)
    first_name = Column(String(64), index=True)
    last_name = Column(String(64), index=True)
    user_role_id = Column(Integer, ForeignKey(UserRole.id))
    is_email_verified = Column(Boolean, default=False)
    is_mobile_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    is_logged_in = Column(Boolean, default=False)
    created_on = Column(DateTime, nullable=False)
    updated_on = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_on = Column(DateTime, nullable=True)
