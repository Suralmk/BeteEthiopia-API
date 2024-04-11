import random
from django.core.mail import EmailMessage

def generate_otp():
    otp = ""
    for _ in range(6):
        otp += str(random.randint(0, 9))
    return otp

def send_otp(email):
    otp = generate_otp()
    email = EmailMessage(
        subject="OTP Request for Password Reset",
        body=f"Here is your OTP to reset your password {otp}",
        from_email="surafelmelaku940@gmail.com",
        to=[email]
    )
    email.send()
    return otp
