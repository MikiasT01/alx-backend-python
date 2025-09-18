from rest_framework import permissions
from .models import Conversation, Message

class IsAuthenticatedParticipant(permissions.BasePermission):
    """Custom permission to ensure only authenticated participants can access and modify conversations and messages."""
    
    def has_permission(self, request, view):
        """Check if the user is authenticated for all API access."""
        if not request.user.is_authenticated:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        """Check object-level permissions based on authentication and participation."""
        if not request.user.is_authenticated:
            return False
        
        # Check for safe methods (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            if isinstance(obj, Conversation):
                return request.user in obj.participants.all()
            if isinstance(obj, Message):
                return request.user in obj.conversation.participants.all()
            return False
        
        # Check for non-safe methods (PUT, PATCH, DELETE, POST)
        if request.method in ['PUT', 'PATCH', 'DELETE', 'POST']:
            if isinstance(obj, Conversation):
                return request.user in obj.participants.all()
            if isinstance(obj, Message):
                return request.user in obj.conversation.participants.all()
            return False
        
        return False