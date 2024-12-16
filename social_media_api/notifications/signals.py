from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from posts.models import Comment, Like
from accounts.models import CustomUser

#Comment notifications
@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(recipient=instance.post.author,
                                    actor = instance.author,
                                    verb = 'added a comment on your post',
                                    target = instance
                                    )
#Like Notification     
@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(recipient=instance.post.author,
                                    actor = instance.user,
                                    verb = 'Liked your post',
                                    target = instance
                                    )
#Follow Notification     
@receiver(post_save, sender=CustomUser)
def create_like_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(recipient=instance.followers,
                                    actor = instance.user,
                                    verb = 'Following you',
                                    target = instance
                                    )
    