from rest_framework import serializers
from .models import Like, Book

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Like
        fields="__all__"

class   BookSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields="__all__"