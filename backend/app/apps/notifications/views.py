from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from app.apps.notifications.models import Notification
from app.apps.notifications.serializers import NotificationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all().order_by("-created_at")
    serializer_class = NotificationSerializer

    @action(detail=True, methods=["patch"])
    def read(self, request, pk=None):
        notice = self.get_object()
        notice.is_read = True
        notice.save(update_fields=["is_read"])
        return Response(NotificationSerializer(notice).data)
