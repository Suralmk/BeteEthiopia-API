from django.core.mail import EmailMessage
import pyotp
from datetime import datetime, timedelta

def send_otp(request, email):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp = totp.now()
    request.session["otp_secret"] = totp.secret
    valid_time = datetime.now() + timedelta(minutes=1)
    request.session["otp_valid"] = str(valid_time)
    email = EmailMessage(
        subject="OTP Request for Password Reset",
        body=f"Here is your OTP to reset your password {otp}",
        from_email="surafelmelaku940@gmail.com",
        to=[email]
    )
    email.send()
    return True

