from rest_framework.permissions import BasePermission, SAFE_METHODS

class PollPermission(BasePermission):
    """
    Custom permission:
    - SAFE_METHODS (GET, HEAD, OPTIONS): anyone can access
    - POST/PUT/DELETE: only the owner (creator) can modify
    - VOTE action: allowed for any authenticated user
    """
    def has_object_permission(self, request, view, obj):
        # Allow all users to read (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        
        # Custom rule for vote action if defined
        if getattr(view, 'action', None) == 'vote':
            return request.user and request.user.is_authenticated

        # Only the owner can write/delete
        return obj.created_by == request.user
