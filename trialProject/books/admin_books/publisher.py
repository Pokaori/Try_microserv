import pika
import sys
import json
from django.conf import settings
url=settings.AMQP_URL
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)




def publish(method,body):
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange='books', exchange_type='direct')
    properties=pika.BasicProperties(method)
    channel.basic_publish(exchange='books', routing_key='likes', body=json.dumps(body),properties=properties)
    connection.close()


