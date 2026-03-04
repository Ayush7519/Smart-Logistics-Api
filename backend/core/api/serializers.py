from core.models.base import AuditLog
from rest_framework import serializers


# -----------------------------------------------------------------------------------------------
# this is admin log serializer.
# -----------------------------------------------------------------------------------------------
class AuditLogSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = AuditLog
        fields = "__all__"
