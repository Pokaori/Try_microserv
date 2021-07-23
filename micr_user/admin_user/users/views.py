from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from .serializers import LoginSerializer, RegistrationSerializer,RefreshSerializer
from .renderers import UserJSONRenderer
from rest_framework import authentication
import jwt
from django.conf import settings
from .tasks import verify_email

from os import path
from .models import User


class RegistrationAPIView(GenericAPIView,viewsets.ViewSet):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)

    def registration(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user=User.objects.get(pk=request.data.get("username",None))

        result = verify_email.delay("".join((request.scheme,"://",request.get_host(), "register",str(user.verification_uuid))), user.email)
        print(result.ready())
        print(result.result)
        return Response({"result":"Email sent!"}, status=status.HTTP_201_CREATED)

    def verify(self,request,uuid):
        print(uuid)
        try:
            user = User.objects.get(verification_uuid=uuid, is_verified=False)
        except User.DoesNotExist:
            return Response({"error":"User does not exist or is already verified"}, status=status.HTTP_404_NOT_FOUND)
        user.is_verified = True
        user.save()
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LoginAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)




class RefreshAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RefreshSerializer

    def get(self, request):
        auth_header = authentication.get_authorization_header(request).split()
        token=auth_header[1]
        payload = jwt.decode(token, settings.SECRET_KEY,algorithms="HS256",options={"verify_signature":False})
        serializer = self.serializer_class(data=payload)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
