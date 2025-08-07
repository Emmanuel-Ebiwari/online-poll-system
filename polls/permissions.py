from rest_framework.permissions import BasePermission, SAFE_METHODS

class PollPermission(BasePermission):
    """
    Permissions:
    - SAFE_METHODS: allowed for everyone
    - POST/PUT/DELETE: allowed only for the poll creator
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in SAFE_METHODS:
            return obj.is_public or obj.created_by == request.user

        return obj.created_by == request.user
    
class QuestionPermission(BasePermission):
    """
    Custom permission for Questions:
    - SAFE_METHODS (GET, HEAD, OPTIONS): 
      • Allowed if the related poll is public or owned by the user
    - POST/PUT/DELETE: 
      • Only allowed if the poll is owned by the user
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        poll = obj.poll_id  # Get related poll

        if request.method in SAFE_METHODS:
            return poll.is_public or poll.created_by == request.user

        return poll.created_by == request.user

class VotePermission(BasePermission):
    """
    Permissions:
    - Any authenticated user can vote (POST)
    - Only the vote creator can update/delete their vote (if supported)
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        poll = obj.poll_id  # Get related poll

        # Only allow voting on public polls or polls created by the user
        return poll.is_public or poll.created_by == request.user
