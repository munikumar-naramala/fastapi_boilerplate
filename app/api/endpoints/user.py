# user.py
from app.models.admin import Admin
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends, Query
from app.models.user import Intern
from app.schemas.user import InternCreate, InternLogin, Interntask, InternTaskStatusUpdate
from app.schemas.common import Token
from app.crud.user import create_access_token_intern, create_intern_task_function, update_task_status_function, delete_intern_task_function
from app.db.base import SessionLocal
from app.api.deps import JWTBearer
from fastapi import HTTPException
from pydantic import ValidationError
from datetime import timedelta
from app.utilities.utils import (
    generate_otp,
    send_otp_email,
    password_hash,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
import smtplib
from fastapi import UploadFile, File
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

user_router = APIRouter()


@user_router.post("/intern/signup/",tags=["Intern"])
async def signup(user: InternCreate):
    db = SessionLocal()
    existing_user = db.query(Intern).filter(Intern.email == user.email).first()

    if existing_user:
        db.close()
        raise HTTPException(status_code=400, detail="User with this email already exists")

    otp = generate_otp()
    send_otp_email(user.email, otp)

    new_user = Intern(
        name=user.name,
        empid=user.empid,
        email=user.email,
        password=password_hash.hash(user.password),
        phone=user.phone,
        position=user.position,
        is_verified=0,
        otp=otp,
    )

    db.add(new_user)
    db.commit()
    db.close()

    return {"message": "OTP sent to your email for verification"}


@user_router.post("/intern/verifyotp/",tags=["Intern"])
async def verify_otp(email: str = Query(...), otp: str = Query(...)):
    db = SessionLocal()
    user = db.query(Intern).filter(Intern.email == email).first()

    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified == 1:
        db.close()
        raise HTTPException(status_code=400, detail="Email already verified")

    if user.otp == otp:
        user.is_verified = 1
        db.commit()
        db.close()
        return {"message": "Email verified"}
    else:
        db.close()
        raise HTTPException(status_code=400, detail="Invalid OTP")

@user_router.post("/intern/login/", response_model=Token,tags=["Intern"])
async def login(form_data: InternLogin):
    db = SessionLocal()
    user = db.query(Intern).filter(Intern.email == form_data.email).first()

    if not user or not password_hash.verify(form_data.password, user.password):
        db.close()
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password",
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token_intern(data={"sub": form_data.email}, expires_delta=access_token_expires)
    db.close()
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.get("/intern/details",tags=["Checking Intern details by Admin"])
async def get_intern_details(current_user: dict = Depends(JWTBearer())):
    if current_user:
        user_email = current_user.get("sub") 

        db = SessionLocal()
        admin = db.query(Admin).filter(Admin.email == user_email).first()
        db.close()

        if not admin:
            raise HTTPException(status_code=403, detail="Only admin users can access this data.")

        # Fetch intern details from the database
        db = SessionLocal()
        interns = db.query(Intern).all()
        db.close()

        intern_data = [
            {
                "name": intern.name,
                "empid": intern.empid,
                "email": intern.email,
                "phone": intern.phone,
                "position": intern.position,
                "task_id": intern.task_id,
                "task_status": intern.task_status
            }
            for intern in interns
        ]

        return {"interns": intern_data}
    else:
        raise HTTPException(status_code=403, detail="Invalid token or expired token.")



@user_router.post("/create/intern/task/{empid}", response_model=Interntask,tags=["Intern Task Management"])
async def select_intern_task(
    empid: str,
    task_data: Interntask,
    current_user: dict = Depends(JWTBearer())
):
    if current_user:
        sub_claim = current_user.get("sub")  # Assuming that "sub" in the token contains the user's email
        if sub_claim:
            email = sub_claim
            return create_intern_task_function(empid, task_data, email)
        else:
            raise HTTPException(status_code=403, detail="Invalid token or expired token")
    else:
        raise HTTPException(status_code=403, detail="Invalid token or expired token")


@user_router.put("/update/task/status/{empid}", response_model=Interntask,tags=["Intern Task Management"])
async def update_task_status_endpoint(
    empid: str,
    task_status_data: InternTaskStatusUpdate,
    current_user: dict = Depends(JWTBearer())
):
    return update_task_status_function(empid, task_status_data, current_user.get("sub"))

@user_router.delete("/delete/intern/task/{empid}",tags=["Intern Task Management"])
async def delete_intern_task_endpoint(
    empid: str,
    current_user: dict = Depends(JWTBearer())
):
    return delete_intern_task_function(empid, current_user.get("sub"))


@user_router.post("/submit/intern/task/{empid}", response_model=Token,tags=["Intern Task Management"])
async def submit_intern_task(
    empid: str,
    file: UploadFile = File(None),
    current_user: dict = Depends(JWTBearer())
):
    if current_user:
        sub_claim = current_user.get("sub")  # Assuming that "sub" in the token contains the user's email
        if sub_claim:
            sender_email = "mysamplemailing@gmail.com"
            sender_password = "ppjgknbbxlrgkjyb"
            recipient_email = "gsivaanandini@gmail.com"

            # Ensure that the current user is an intern with the matching empid
            db = SessionLocal()
            intern = db.query(Intern).filter(Intern.email == sub_claim, Intern.empid == empid).first()
            db.close()

            if not intern:
                raise HTTPException(status_code=403, detail="Only interns with matching empid can create tasks")

            # Retrieve task_id and task_status from the intern
            task_id = intern.task_id
            task_status = intern.task_status

            # Send email with attachments and intern's information
            subject = f"{empid} Task Details"
            message = f"Task ID: {task_id}\nTask Status: {task_status}\nPlease find the task details attached."

            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = recipient_email
            msg["Subject"] = subject

            msg.attach(MIMEText(message, "plain"))

            if file:
                attachment_data = file.file.read()
                attachment_name = file.filename

                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment_data)
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{attachment_name}"')

                msg.attach(part)

            try:
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, recipient_email, msg.as_string())
                return {"access_token": "Email sent successfully", "token_type": "bearer"}
            except Exception as e:
                return HTTPException(status_code=500, detail=f"Email sending error: {str(e)}")
            except ValidationError as e:
                for error in e.errors():
                    if error["loc"] == ("response", "token_type"):
                        print("Mail sent successfully")
