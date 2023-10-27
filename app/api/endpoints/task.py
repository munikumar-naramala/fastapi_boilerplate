from fastapi import APIRouter, Depends
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdateResponse, TaskDeleteResponse, TaskUpdateData
from app.api.deps import JWTBearer
from fastapi import HTTPException
from app.db.base import SessionLocal, get_db
from sqlalchemy.orm import Session
from app.crud.task import (
    create_task,
    get_all_tasks,
    update_task,
    delete_task
)
from app.models.admin import Admin


task_router = APIRouter()

@task_router.post("/create/task/", response_model=TaskCreate)
async def create_task_endpoint(
    task_data: TaskCreate, current_user: dict = Depends(JWTBearer())
):
    if current_user:
        sub_claim = current_user.get("sub")
        if sub_claim:
            user_email = sub_claim
            try:
                db = SessionLocal()
                admin = db.query(Admin).filter(Admin.email == user_email).first()
                if not admin:
                    raise HTTPException(status_code=403, detail="Only admin users can create tasks")

                db.add(Task(
                    task_id=task_data.task_id,
                    name=task_data.name,
                    description=task_data.description
                ))
                db.commit()


                return {
                    "name": task_data.name,
                    "task_id": task_data.task_id,
                    "description": task_data.description
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    else:
        raise HTTPException(status_code=403, detail="Invalid token or expired token.")
@task_router.get("/task/details")
async def get_task_details(db: Session = Depends(get_db)):
    tasks = get_all_tasks(db)
    # Format and return the task data
    task_data = [
        {
            "task_id": task.task_id,
            "name": task.name,
            "description": task.description
        }
        for task in tasks
    ]
    return {"TASKS": task_data}


@task_router.put("/update/task/{task_id}", response_model=TaskUpdateResponse)
async def update_task_endpoint(
    task_id: str, task_data: TaskUpdateData, current_user: dict = Depends(JWTBearer())
):
    if current_user:
        sub_claim = current_user.get("sub")
        if sub_claim:
            user_email = sub_claim
            try:
                db = SessionLocal()
                admin = db.query(Admin).filter(Admin.email == user_email).first()
                if not admin:
                    raise HTTPException(status_code=403, detail="Only admin users can update tasks")

                updated_task = update_task(db, task_id, task_data)
                db.close()

                if not updated_task:
                    raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")

                return updated_task
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    else:
        raise HTTPException(status_code=403, detail="Invalid token or expired token.")

@task_router.delete("/delete/task/{task_id}", response_model=TaskDeleteResponse)
async def delete_task_endpoint(
    task_id: str, current_user: dict = Depends(JWTBearer())
):
    if current_user:
        sub_claim = current_user.get("sub")
        if sub_claim:
            user_email = sub_claim
            try:
                db = SessionLocal()
                admin = db.query(Admin).filter(Admin.email == user_email).first()
                if not admin:
                    raise HTTPException(status_code=403, detail="Only admin users can delete tasks")

                deleted_task = delete_task(db, task_id)
                db.close()

                if not deleted_task:
                    raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")

                return deleted_task
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    else:
        raise HTTPException(status_code=403, detail="Invalid token or expired token.")