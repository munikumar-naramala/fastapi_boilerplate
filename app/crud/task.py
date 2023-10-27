from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdateData, TaskDeleteResponse
from fastapi import HTTPException

def create_task(db: Session, task_data: TaskCreate):
    db.add(Task(
        task_id=task_data.task_id,
        name=task_data.name,
        description=task_data.description
    ))
    db.commit()
    return task_data


def get_all_tasks(db: Session):
    return db.query(Task).all()

def get_task_by_id(db: Session, task_id: str):
    return db.query(Task).filter(Task.task_id == task_id).first()
def update_task(db_session, task_id: str, task_data: TaskUpdateData):
    task = db_session.query(Task).filter(Task.task_id == task_id).first()
    if task:
        task.name = task_data.name
        task.description = task_data.description
        db_session.commit()
        return {
            "task_id": task_id,
            "name": task_data.name,
            "description": task_data.description
        }


def delete_task(db: Session, task_id: str):
    task = get_task_by_id(db, task_id)
    if task:
        db.delete(task)
        db.commit()
        return TaskDeleteResponse(task_id=task.task_id)
    else:
        raise HTTPException(status_code=404, detail="Task not found")

