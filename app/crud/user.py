from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.db.base import SessionLocal
from app.models.user import Intern
from app.schemas.user import Interntask, InternTaskStatusUpdate
from fastapi import HTTPException

SECRET_KEY = "placeholder-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
password_hash = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token_intern(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_intern_task_function(empid: str, task_data: Interntask, email: str):
    try:
        db = SessionLocal()
        intern = db.query(Intern).filter(Intern.empid == empid, Intern.email == email).first()
        if not intern:
            raise HTTPException(status_code=403, detail="Only interns with matching empid can create tasks")

        task_id = task_data.task_id
        task_status = task_data.task_status

        # Update the intern's task information
        intern.task_id = task_id
        intern.task_status = task_status

        # Commit the changes to the database
        db.commit()
        db.refresh(intern)

        return {"task_id": task_id, "task_status": task_status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")



def update_task_status_function(empid: str, task_status_data: InternTaskStatusUpdate, email: str):
    try:
        db = SessionLocal()
        intern = db.query(Intern).filter(Intern.empid == empid, Intern.email == email).first()
        if not intern:
            raise HTTPException(status_code=403, detail="Only interns with matching empid can update task status")

        # Update the task_status
        intern.task_status = task_status_data.task_status

        # Commit the changes to the database
        db.commit()
        db.refresh(intern)

        return {"task_id": intern.task_id, "task_status": intern.task_status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Delete function
def delete_intern_task_function(empid: str, email: str):
    try:
        db = SessionLocal()
        intern = db.query(Intern).filter(Intern.empid == empid, Intern.email == email).first()
        if not intern:
            raise HTTPException(status_code=404, detail="Intern not found")

        # Delete the intern's task information
        intern.task_id = None
        intern.task_status = None

        # Commit the changes to the database
        db.commit()
        db.refresh(intern)

        return {"message": "Task deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


