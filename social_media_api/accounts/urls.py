from django.urls import path, include
from .views import RegisterView
from .views import LoginView
from .views import ProfileView
from .views import FollowView, LikeView
from notifications.views import NotificationViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'notifications',NotificationViewset,basename='notification')


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('api-token-auth/', LoginView.as_view(), name='api_token_auth'),
    path('follow/<int:user_id>/',FollowView.as_view(),name='follow'),
    path('unfollow/<int:user_id>/',FollowView.as_view(),name='unfollow'),
    path('posts/<int:pk>/like/',LikeView.as_view(),name='like'),
    path('posts/<int:pk>/unlike/',LikeView.as_view(),name='unlike'),
    path('', include(router.urls)),
]
