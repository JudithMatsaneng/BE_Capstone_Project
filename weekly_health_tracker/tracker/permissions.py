from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        user_id = getattr(obj, "user_id", None) or getattr(obj, "owner_id", None)
        if user_id is None:
            return False
        return user_id == request.user.id

