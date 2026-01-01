from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.utils import timezone
from datetime import timedelta
from product.models import Product

class CanCreateProduct(BasePermission):
    def has_permission(self, request, view):
        if request.method != "POST":
            return True

        if not request.user.is_authenticated:
            return False
        
        if Product.objects.filter(poster=request.user).count() >= 5:
           return False
        return True
    
class IsOwnerOrModerator(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        if request.user.is_staff:
            return True
        
        return obj.poster == request.user
    

class IsAuthenticatedOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )

allowed_methods = ["GET", "PUT", "PATCH", "DELETE"]
class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST" and request.user.is_staff:
            return False
        
        if request.method == "POST" and not request.user.is_staff:
            return True
        
        if request.method in allowed_methods and request.user.is_staff:
           return True

class CanEditIn(BasePermission):
    def has_object_permission(self, request, view, obj):
        time_passed = timezone.now() - obj.created_at
        return time_passed <= timedelta(minutes=2)
        