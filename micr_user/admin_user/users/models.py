import jwt
import uuid
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager, PermissionsMixin
)

from django.db import models

class UserManager(BaseUserManager):

    def create_user(self, username, email, password):

        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        if password is None:
            raise TypeError('Users must have an password.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):

        user = self.create_user(username, email, password)
        is_superuser=True
        user.save()

        return user

class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField( primary_key=True,unique=True,max_length=255)

    email = models.EmailField( unique=True)

    password = models.CharField(max_length=255)
    is_verified = models.BooleanField( default=False)
    verification_uuid = models.UUIDField(default=uuid.uuid4)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password','email']

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()


    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(minutes=15)
        print(settings.SECRET_KEY)
        token = jwt.encode({
            'username': self.pk,
            'exp': dt.utcfromtimestamp(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')

        return token
