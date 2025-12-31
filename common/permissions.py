from rest_framework.permissions import *
from users.models import CustomUser


class IsOwnerOrModerator(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        if request.user.is_staff == True:
            return True
        
        return obj.poster == request.user
    

class IsAuthenticatedOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )

class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST" and request.user.is_staff:
            return False
