from django.db import models
from django.contrib.auth.models import AnonymousUser

class Author(models.Model):
    picture=models.URLField()
    fullname=models.CharField(max_length=200)
    birth=models.DateField()
    death=models.DateField(null=True)
    describe=models.TextField()

class Subscriber(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True)

class Books(models.Model):
    picture=models.URLField()
    title=models.CharField(max_length=200)
    year=models.PositiveIntegerField()
    opinion=models.TextField()
    time_publish=models.DateTimeField()
    id_author = models.ForeignKey(to=Author, on_delete=models.CASCADE)
    username_publisher=models.CharField(max_length=255)

class ServerUser(AnonymousUser):

    @property
    def is_authenticated(self):
        return True

