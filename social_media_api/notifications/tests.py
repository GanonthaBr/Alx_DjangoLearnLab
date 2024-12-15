from django.test import TestCase
from posts.models import Like
from notifications.models import Notification
from accounts.models import CustomUser

# Create your tests here.

user1  = CustomUser.objects.get(username='Bruno')
user2 = CustomUser.objects.get(username='Gano')

like = Like.objects.first()

Notification.objects.create(
    recipient = user1,
    actor = user2,
    verb = 'Has liked',
    target = like,
)
