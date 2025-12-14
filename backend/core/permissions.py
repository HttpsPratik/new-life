
from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    #Permission to only allow owners of an object or admins to edit/delete it.
 
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if user is admin
        if request.user.is_staff or request.user.role == 'ADMIN':
            return True
        
        # Check if user is the owner
        # Handle different owner field names
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        elif hasattr(obj, 'reporter'):
            return obj.reporter == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'donor'):
            return obj.donor == request.user
        
        return False


class HasAcceptedTerms(permissions.BasePermission):
    
    message = "You must accept the latest Terms & Conditions to perform this action."
    
    def has_permission(self, request, view):
        # Allow read-only methods
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return False
        
        # Check if user has accepted terms
        return request.user.terms_accepted


class IsAdminUser(permissions.BasePermission):
    #Permission to only allow admin users.
   
    message = "Only admin users can perform this action."
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.is_staff or request.user.role == 'ADMIN'
        )