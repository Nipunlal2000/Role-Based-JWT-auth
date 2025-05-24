from django.core.mail import send_mail
from django.conf import settings
import random
 
def send_otp_email(email, otp):
    subject = 'Your OTP Code'
    message = f'Your OTP code is {otp}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
 
def generate_otp():
    return random.randint(100000, 999999)
 
def send_password_reset(email , reset_link):
    subject = 'Password Reset Request'
    message = f'Click the link below to reset your password:\n{reset_link}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)