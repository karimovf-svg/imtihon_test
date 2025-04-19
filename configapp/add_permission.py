from rest_framework.permissions import BasePermission

class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        if getattr(request.user, 'is_admin', False):
            return True

        return False