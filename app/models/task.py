from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(128))
    empid = Column(String(32), index=True)
    email = Column(String(128), index=True)
    task = Column(String(128))
    description = Column(String(256))
