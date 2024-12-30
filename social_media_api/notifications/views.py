from rest_framework import viewsets, permissions
from .models import Notification
from .serializers import NotificationSerializer

# Create your views here.
class NotificationViewset(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)
