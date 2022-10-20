from lib2to3.pytree import Base
from rest_framework.permissions import BasePermission

from api.models import Student

class IsOwnerOfQuestion(BasePermission):
    def has_object_permission(self,request, view, obj):
        if request.user:
            if request.user.is_superuser:
                return True
            else:
                student = Student.objects.get(user=request.user)
                return obj.student == student
        else:
            return False

    # return bool(request.user and request.user.is_authenticated)