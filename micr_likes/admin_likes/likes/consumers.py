
import pika
import os
import sys
import json
sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE','admin_likes.settings')

import django
django.setup()
from django.conf import settings

url=settings.AMQP_URL

from likes.serializers import BookSerializer, Book


def callback(ch,method,properties,body):
    print(body)
    if properties.content_type=='create_post':
        serializer = BookSerializer(data=json.loads(body))
        serializer.is_valid(raise_exception=True)
        serializer.save()
    elif properties.content_type=='delete_post':
        try:
            book = Book.objects.get(id=json.loads(body)["id"])
        except Exception as exc:
            print(exc)
        book.delete()


params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()


result = channel.queue_declare(queue='likes',durable = True)
channel.queue_bind(queue='likes', exchange='books', routing_key = 'likes')
queue_name = result.method.queue

channel.basic_consume( queue=queue_name, on_message_callback=callback,auto_ack=True)
channel.start_consuming()
channel.close()

