from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Books, Author,Subscriber
from .serializers import BooksSerializer, AuthorSerializer,SubscriberSerializer
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import authentication
import jwt
from rest_framework.generics import GenericAPIView
from django.conf import settings
from .publisher import publish
from .tasks import send_telegram_review

class BookViewSet(viewsets.ViewSet,GenericAPIView ):
    permission_classes_by_action = {'get_all_books': [AllowAny],
                                    'get_book': [AllowAny],
                                    'default': [IsAuthenticated]}
    serializer_class =BooksSerializer

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes_by_action['default']]

    def get_all_books(self,request):
        books=Books.objects.all()
        serializer= self.serializer_class(books,many=True)
        return Response(serializer.data)

    def get_all_user_books(self,request):
        auth_header = authentication.get_authorization_header(request).split()
        token = auth_header[1].decode('utf-8')
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
        books=Books.objects.filter(username_publisher=payload["username"])
        serializer= self.serializer_class(books,many=True)
        return Response(serializer.data)

    def new_book(self,request):
        auth_header = authentication.get_authorization_header(request).split()
        token = auth_header[1].decode('utf-8')
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
        request.data.update({"username_publisher":payload["username"]})
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish("create_post",{"id":serializer.data["id"]})
        subscribers=Subscriber.objects.all()

        result=serializer.data
        result["url"]="".join((request.scheme,'://',request.get_host(),"/api/book/",str(serializer.data["id"])))
        serializer2 = SubscriberSerializer(subscribers,many=True)
        res=send_telegram_review.delay(serializer2.data,result)
        return Response(serializer.data, status.HTTP_201_CREATED)

    def get_book(self,request,pk=None):
        try:
            book = Books.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(book)
        return Response(serializer.data)

    def delete_book(self,request,pk=None):
        try:
            auth_header = authentication.get_authorization_header(request).split()
            token = auth_header[1].decode('utf-8')
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            book = Books.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if book.username_publisher!=payload["username"]:
            return Response({"error":"You are not owner of this posts."},status.HTTP_405_METHOD_NOT_ALLOWED)
        book.delete()
        publish("delete_post",{"id":pk})
        return Response(status=status.HTTP_204_NO_CONTENT)

class AuthorViewSet(viewsets.ViewSet,GenericAPIView):
    serializer_class = AuthorSerializer
    def get_all_authors(self,request):
        authors=Author.objects.all()
        serializer= self.serializer_class(authors,many=True)
        return Response(serializer.data)

    def new_author(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

    def get_author(self,request,pk=None):
        try:
            author = Author.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer =self.serializer_class(author)
        return Response(serializer.data)

    def delete_author(self,request,pk=None):
        try:
            author = Author.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    #
    # {
    #     "picture": "https://archive.org/services/img/my_first_book_1006_librivox/full/pct:500/0/default.jpg",
    #     "title": "First",
    #     "year": "2021",
    #     "opinion": "Cool",
    #     "time_publish": "2021-04-18 12:23:23"
    #
    # }

# {
#     "picture":"https://i.pinimg.com/originals/9f/ec/93/9fec939c1dbf5d2f3f75952d8baf1890.png",
#     "fullname":"Fyodor Dostoevskiy",
#     "birth":"1821-11-11",
#     "death":"1881-02-09",
#     "describe":"Cool life"
# }

