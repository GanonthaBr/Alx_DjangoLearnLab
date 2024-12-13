from django.urls import path
from .views import RegisterView
from .views import LoginView
from .views import ProfileView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('api-token-auth/', LoginView.as_view(), name='api_token_auth'),
]