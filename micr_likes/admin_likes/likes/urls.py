from django.contrib import admin
from django.urls import path
from .views import LikeViewSet
urlpatterns = [
    path('',LikeViewSet.as_view({
        'get':'get_all_likes',
        'post':'new_like'
    }) ),
    path('<int:id_book>/',LikeViewSet.as_view({
        'get':'get_like',
        'delete':'delete_like'
    })),
]