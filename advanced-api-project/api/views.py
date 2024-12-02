from django.shortcuts import render
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

#filtering, searching and ordering
'''
    pip install django-filter
    add django_filters to APPS
    update settings.py for filters and ordering
'''
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework, filters

# Create your views here.

#list all Books
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    #adding filter backends for search, filter and ordering
    filter_backends = [rest_framework.DjangoFilterBackend, SearchFilter, filters.OrderingFilter]

    # search fields
    search_fields = ['title','author']

    # filterset fields
    filterset_fields = ['publication_year','author']

    # ordering fields
    ordering_fields = ['title','publication_year']

#Retrieve a single Book by Id
class BookDetailsView(generics.DetailView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


#Create a new Book
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
        return super().perform_create(serializer)


#Update an existing Book
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save()
        return super().perform_update(serializer)

#Delete a Book
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]