
from books.my_celery  import app
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE','books.settings')

import django
django.setup()
from .subscribe_bot import send_review
import json

@app.task
def send_telegram_review(subscribers,book):
    send_review(subscribers,book)
    return "Sent"