from passlib.context import CryptContext
from jose import jwt
import string
import random
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

SECRET_KEY = "placeholder-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
password_hash = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_otp():
    return ''.join(random.choices(string.digits, k=4))

def send_otp_email(email, otp):
    # Your email sending code here
    sender_email = "mysamplemailing@gmail.com"
    sender_password = "ppjgknbbxlrgkjyb"
    subject = "Email Verification OTP"
    message = f"Your OTP for email verification is: {otp}"
    msg = MIMEMultipart()
    msg.attach(MIMEText(message, "plain"))
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = subject

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())
    except Exception as e:
        print(f"Email sending error: {str(e)}")

def send_email(sender_email, sender_password, recipient_email, subject, message):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

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
        print(f"Email sending error: {str(e)}")

