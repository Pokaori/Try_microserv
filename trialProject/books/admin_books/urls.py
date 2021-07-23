from django.contrib import admin
from django.urls import path
from .views import BookViewSet, AuthorViewSet
urlpatterns = [
    path('book/',BookViewSet.as_view({
        'get':'get_all_books',
        'post':'new_book'
    }) ),
    path('book/<int:pk>/',BookViewSet.as_view({
        'get':'get_book',
        'delete':'delete_book'
    })),
    path('book/user/',BookViewSet.as_view({
        'get':'get_all_user_books',
    })),
    path('author/', AuthorViewSet.as_view({
        'get': 'get_all_authors',
        'post': 'new_author'
    })),
    path('author/<int:pk>', AuthorViewSet.as_view({
        'get': 'get_author',
        'delete': 'delete_author'
    }))
]