from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Like
from .serializers import LikeSerializer
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import authentication
import jwt
from rest_framework.generics import GenericAPIView
from django.conf import settings

class LikeViewSet(viewsets.ViewSet,GenericAPIView):
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated,)
    def get_all_likes(self,request):
        auth_header = authentication.get_authorization_header(request).split()
        token = auth_header[1].decode('utf-8')
        payload = jwt.decode(token, settings.SECRET_KEY,algorithms="HS256")
        likes = Like.objects.filter(username=payload["username"])
        serializer= self.serializer_class(likes,many=True)
        return Response(serializer.data)

    def new_like(self,request):
        try:
            auth_header = authentication.get_authorization_header(request).split()
            token = auth_header[1].decode('utf-8')
            payload = jwt.decode(token, settings.SECRET_KEY,algorithms="HS256")
            Like.objects.get(id_book=request.data["id_book"],username=payload["username"])
        except ObjectDoesNotExist:
            serializer = self.serializer_class(data={"username":payload["username"],"id_book":request.data["id_book"]})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response({"error":"like already exist"},status.HTTP_400_BAD_REQUEST)


    def get_like(self,request,id_book):
        try:
            auth_header = authentication.get_authorization_header(request).split()
            token = auth_header[1].decode('utf-8')
            payload = jwt.decode(token, settings.SECRET_KEY,algorithms="HS256")
            like = Like.objects.get(id_book=id_book, username=payload["username"])
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(like)
        return Response(serializer.data)

    def delete_like(self,request,id_book):
        try:
            auth_header = authentication.get_authorization_header(request).split()
            token = auth_header[1].decode('utf-8')
            payload = jwt.decode(token, settings.SECRET_KEY,algorithms="HS256")
            like = Like.objects.get(id_book=id_book, username=payload["username"])
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


