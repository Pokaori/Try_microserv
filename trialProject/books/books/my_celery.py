
from __future__ import absolute_import
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE','books.settings')

import django
django.setup()

from django.conf import settings

app = Celery('books',
             broker=settings.AMQP_URL,
             backend='rpc://',
             include=['admin_books.tasks'])