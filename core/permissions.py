from rest_framework.permissions import BasePermission


class SuperuserPermission(BasePermission):
    message = "Do not have permission"

    def has_permission(self, request, view):
        user = request.user
        return user.is_superuser


class UserUpdatingPermission(BasePermission):
    message = "Do not have permission to update/delete this user!"

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser or user == obj:
            return True
        return False
