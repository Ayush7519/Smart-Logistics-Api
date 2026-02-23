from rest_framework.permissions import BasePermission
from users.models.user_model import User


# -----------------------------------------------------------------------------------------------
# this is the admin permission calss.
# -----------------------------------------------------------------------------------------------
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.ADMIN


# -----------------------------------------------------------------------------------------------
# this is the manager permission class.
# -----------------------------------------------------------------------------------------------
class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.MANAGER


# -----------------------------------------------------------------------------------------------
# this is the driver permission class.
# -----------------------------------------------------------------------------------------------
class IsDriver(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.DRIVER
