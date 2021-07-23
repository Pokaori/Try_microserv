from django.urls import path
from django.contrib import admin
from .views import LoginAPIView, RegistrationAPIView,RefreshAPIView
import uuid

app_name = 'authentication'
urlpatterns = [
    path('register/', RegistrationAPIView.as_view({'post':'registration',
    })),
    path('login/', LoginAPIView.as_view()),
    path('refresh/', RefreshAPIView.as_view()),
    path('register/<uuid:uuid>', RegistrationAPIView.as_view({
        'get':'verify'
    }))
]