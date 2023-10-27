from pydantic import BaseModel, EmailStr

class AdminCreate(BaseModel):
    name: str
    empid: str
    email: EmailStr
    password: str
    phone: str
    position: str

class AdminLogin(BaseModel):
    email: EmailStr
    password: str



