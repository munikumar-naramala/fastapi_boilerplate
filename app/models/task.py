from sqlalchemy import Column, Integer, String
from app.db.base import Base


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String(128), unique=True)
    name = Column(String(128))
    description = Column(String(256))
