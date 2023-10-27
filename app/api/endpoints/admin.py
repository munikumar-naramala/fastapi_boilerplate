from fastapi import APIRouter, Query, Depends
from fastapi.security import OAuth2PasswordBearer
from app.schemas.admin import AdminCreate, AdminLogin
from app.schemas.common import Token
from app.models.admin import Admin
from app.models.user import Intern
from app.crud.admin import create_access_token_admin
from app.db.base import SessionLocal
from app.api.deps import JWTBearer
from fastapi import HTTPException
from datetime import timedelta
from app.utilities.utils import (
    generate_otp,
    send_otp_email,
    password_hash,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


admin_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@admin_router.post("/admin/signup/", tags=["Admin"])
async def signup(user: AdminCreate):
    db = SessionLocal()
    existing_user = db.query(Admin).filter(Admin.email == user.email).first()

    if existing_user:
        db.close()
        raise HTTPException(status_code=400, detail="User with this email already exists")

    otp = generate_otp()
    send_otp_email(user.email, otp)

    new_user = Admin(
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



@admin_router.post("/admin/verifyotp/", tags=["Admin"])
async def verify_otp(email: str = Query(...), otp: str = Query(...)):
    db = SessionLocal()
    user = db.query(Admin).filter(Admin.email == email).first()

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

@admin_router.post("/admin/login/", response_model=Token, tags=["Admin"])
async def login(form_data: AdminLogin):
    db = SessionLocal()
    user = db.query(Admin).filter(Admin.email == form_data.email).first()

    if not user or not password_hash.verify(form_data.password, user.password):
        db.close()
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password",
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token_admin(data={"sub": form_data.email}, expires_delta=access_token_expires)
    db.close()
    return {"access_token": access_token, "token_type": "bearer"}



@admin_router.post("/admin/evaluation/", tags=["Task Evaluation"])
async def evaluation(
    empid: str,
    email: str,
    project_selection_outof_10: int,
    coding_way_outof_10: int,
    module_organization_outof_10: int,
    remarks: str,
    current_user: dict = Depends(JWTBearer())
):
    if current_user:
        admin_email = current_user.get("sub")  # Assuming that "sub" in the token contains the admin's email

        # Fetch the intern's email from the Intern table
        db = SessionLocal()
        intern = db.query(Intern).filter(Intern.empid == empid, Intern.email == email).first()

        if not intern:
            db.close()
            raise HTTPException(status_code=404, detail="Intern not found")

        recipient_email = intern.email
        db.close()

        # Perform your email operations
        subject = "Intern Evaluation"
        sender_email = "mysamplemailing@gmail.com"
        sender_password = "ppjgknbbxlrgkjyb"

        message = f"Empid: {empid}\n"
        message += f"Project Selection: {project_selection_outof_10}\n"
        message += f"Coding Way: {coding_way_outof_10}\n"
        message += f"Module Organization: {module_organization_outof_10}\n"
        message += f"Overall: {project_selection_outof_10 + coding_way_outof_10 + module_organization_outof_10}\n"
        message += f"Remarks: {remarks}\n"

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject

        msg.attach(MIMEText(message, "plain"))

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_email, msg.as_string())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Email sending error: {str(e)}")

        # Perform other operations, such as saving the evaluation details, in your database here

        return {"message": "Evaluation email sent successfully"}
    else:
        raise HTTPException(status_code=403, detail="Invalid token or expired token")