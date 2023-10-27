from pydantic import BaseModel, EmailStr

class InternCreate(BaseModel):
    name: str
    empid: str
    email: EmailStr
    password: str
    phone: str
    position: str

class InternLogin(BaseModel):
    email: EmailStr
    password: str

class Interntask(BaseModel):
    task_id: str
    task_status: str

class InternTaskStatusUpdate(BaseModel):
    task_status: str


