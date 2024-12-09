from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('',views.home,name='home'),
    path('posts/new/',PostCreateView.as_view(),name='post-create'),
    path('posts/',PostListView.as_view(),name='posts'),
    path('posts/<int:pk>/',PostDetailView.as_view(),name='post-detail'),
    path('posts/<int:pk>/edit/',PostUpdateView.as_view(),name='post-edit'),
    path('posts/<int:pk>/delete/',PostDeleteView.as_view(),name='post-delete'),
    path('profile/',views.profile_view,name='profile')
]