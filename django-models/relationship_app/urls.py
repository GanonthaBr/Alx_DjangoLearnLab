from django.urls import path
from . import views
from .views import LibrairyDetails

urlpatterns = [
    path('books/',views.books,name='book-list'),
    path('library/<int:pk>',LibrairyDetails.as_view(),name='library-details')
]