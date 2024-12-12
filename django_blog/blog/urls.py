from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',auth_views.LoginView.as_view(template_name='blog/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='blog/login.html'),name='logout'),
    path('register/',views.register,name='register'),
    path('posts/new/',PostCreateView.as_view(),name='post-create'),
    path('posts/',PostListView.as_view(),name='posts'),
    path('posts/<int:pk>/',PostDetailView.as_view(),name='post-detail'),
    path('post/<int:pk>/edit/',PostUpdateView.as_view(),name='post-edit'),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(),name='post-delete'),
    path('profile/',views.profile_view,name='profile'),
    path('comment/<int:pk>/edit/',CommentUpdateView.as_view(),name='comment-edit'),
    path('comment/<int:pk>/delete/',CommentDeleteView.as_view(),name='comment-delete')
]