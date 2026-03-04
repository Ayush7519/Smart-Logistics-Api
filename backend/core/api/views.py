from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from core.models.base import AuditLog
from core.api.serializers import AuditLogSerializer
from users.permission import IsAdmin


class AuditLogListView(ListAPIView):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
