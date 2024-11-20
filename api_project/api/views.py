from django.shortcuts import render
from rest_framework import generics, viewsets
from .serializers import BookSerializer
from .models import Book
from rest_framework.permissions import IsAdminUser, IsAuthenticated

# Create your views here.

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    #Apply permissions
    permission_classes = [IsAuthenticated]


    def get_permissions(self):
        if self.action in ['create','update','destroy','partial_update']:
            return [IsAdminUser()]
        return super().get_permissions()