from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('',views.home,name='posts'),
    path('profile/',views.profile_view,name='profile')
]