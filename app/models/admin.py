from sqlalchemy import Column, String, Integer
from app.db.base import Base

class Admin(Base):
    __tablename__ = 'admin'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128))
    empid = Column(String(128), unique=True)
    email = Column(String(128), unique=True)
    password = Column(String(128))
    phone = Column(String(128))
    position = Column(String(128))