from rest_framework import serializers

from .models import User
from django.contrib.auth import authenticate
from rest_framework import authentication, exceptions

class RegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        user=User.objects.create_user(**validated_data)
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }

class LoginSerializer(serializers.Serializer):
        email = serializers.CharField(max_length=255,read_only=True)
        username = serializers.CharField(max_length=255)
        password = serializers.CharField(max_length=128, write_only=True)
        token = serializers.CharField(max_length=255, read_only=True)

        def validate(self, data):
            print(data)
            username = data.get('username', None)
            password = data.get('password', None)

            if username is None:
                raise serializers.ValidationError(
                    'A username is required to log in.'
                )

            if password is None:
                raise serializers.ValidationError(
                    'A password is required to log in.'
                )

            user = authenticate(username=username, password=password)

            if user is None:
                raise serializers.ValidationError(
                    'A user with this username and password was not found.'
                )
            return {
                'email': user.email,
                'username': user.username,
                'token': user.token
            }

class RefreshSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255, read_only=True)
    username = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ['token','username']

    def validate(self, data):
        user=User.objects.get(pk=data['username'])
        return {
            'token': user.token
        }
