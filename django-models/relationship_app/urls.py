from django.urls import path
from . import views
from .views import LibrairyDetails
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('books/',views.books,name='book-list'),
    path('library/<int:pk>',LibrairyDetails.as_view(),name='library-details'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    
]