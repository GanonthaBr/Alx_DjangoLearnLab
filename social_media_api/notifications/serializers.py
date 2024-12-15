from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField() #display the actor username
    target = serializers.StringRelatedField() #display the target's string representation

    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'actor', 'verb', 'target', 'timestamp'
        ]