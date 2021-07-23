from django.db import models
from django.contrib.auth.models import AnonymousUser


class ServerUser(AnonymousUser):
    @property
    def is_authenticated(self):
        return True


class Book(models.Model):
    id = models.PositiveIntegerField( primary_key=True, unique=True)


class Like(models.Model):
    id_book = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)

