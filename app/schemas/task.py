from pydantic import BaseModel

class TaskCreate(BaseModel):
    task_id: str
    name: str
    description: str

class TaskUpdateResponse(BaseModel):
    task_id: str
    name: str
    description: str

class TaskDeleteResponse(BaseModel):
    task_id: str
    name: str = None
    description: str = None

class TaskUpdateData(BaseModel):
    name: str
    description: str
