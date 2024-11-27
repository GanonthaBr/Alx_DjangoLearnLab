from django.urls import path
from .views import BookCreateView
from .views import BookListView
from .views import BookDeleteView
from .views import BookDetailsView
from .views import BookUpdateView

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('books/',BookListView.as_view(),name='book-list'),
    path('books/<int:pk>',BookDetailsView.as_view(),name='book-detail'),
    path('books/create/',BookCreateView.as_view(),name='book-create'),
    path('books/<int:pk>/update/',BookUpdateView.as_view(),name='book-update'),
    path('books/<int:pk>/delete/',BookDeleteView.as_view(),name='book-delete'),
    path('api-auth-token/',obtain_auth_token,name='api_auth_token')

]


