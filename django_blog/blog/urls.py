from django.urls import path
from . import views
from .views import *
from .views import PostByTagListView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',auth_views.LoginView.as_view(template_name='blog/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='blog/login.html'),name='logout'),
    path('register/',views.register,name='register'),
    path('post/new/',PostCreateView.as_view(),name='post-create'),
    path('posts/',PostListView.as_view(),name='posts'),
    path('posts/<int:pk>/',PostDetailView.as_view(),name='post-detail'),
    path('post/<int:pk>/update/',PostUpdateView.as_view(),name='post-edit'),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(),name='post-delete'),
    path('profile/',views.profile_view,name='profile'),
    path('comment/<int:pk>/update/',CommentUpdateView.as_view(),name='comment-edit'),
    path('comment/<int:pk>/delete/',CommentDeleteView.as_view(),name='comment-delete'),
    path('post/<int:pk>/comments/new/',CommentCreateView.as_view(),name='comment-reply'),
    path('tags/<slug:tag_slug>/',PostByTagListView.as_view(),name='posts-by-tag'),
    path('search/',views.search,name='search'),
   

]