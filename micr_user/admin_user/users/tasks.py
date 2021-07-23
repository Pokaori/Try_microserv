
from admin_user.celery  import app
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE','admin_user.settings')

import django
django.setup()
from django.conf import settings
from django.core.mail import send_mail

@app.task
def verify_email(url,email):
    subject = 'Welcome to SharingBooks'
    message = f'Please verify your email\n {url}'
    send_mail(subject,
              message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
    return "Sent"