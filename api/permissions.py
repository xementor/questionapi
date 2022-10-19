from lib2to3.pytree import Base
from rest_framework.permissions import BasePermission

class isOwnerOfthePost(BasePermission):
    def has_permission(self, request, view):
        return True

    # return bool(request.user and request.user.is_authenticated)