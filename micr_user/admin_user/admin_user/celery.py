
from __future__ import absolute_import
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE','admin_user.settings')

import django
django.setup()
from django.conf import settings

app = Celery('admin_user',
             broker=settings.AMQP_URL,
             backend='rpc://',
             include=['users.tasks'])


