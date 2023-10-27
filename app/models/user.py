from sqlalchemy import Column, String, Integer, ForeignKey,  LargeBinary
from sqlalchemy.orm import relationship
from app.db.base import Base

class Intern(Base):
    __tablename__ = 'interns'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128))
    empid = Column(String(128), unique=True)
    email = Column(String(128), unique=True)
    password = Column(String(128))
    phone = Column(String(128))
    position = Column(String(128))
    task_id = Column(String(128), ForeignKey('task.task_id'))
    task_status = Column(String(128))
    #document_submission = Column(LargeBinary)

    task = relationship("Task")