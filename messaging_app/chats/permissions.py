# Django-Middleware-0x03/chats/permissions.py
from rest_framework import permissions
from .models import Conversation, Message

class IsAuthenticatedParticipant(permissions.BasePermission):
    """Custom permission to ensure only authenticated participants can access and modify conversations and messages."""
    
    def has_permission(self, request, view):
        """Check if the user is authenticated for all API access."""
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Check object-level permissions based on authentication and participation."""
        if not request.user.is_authenticated:
            return False
        
        if request.method in permissions.SAFE_METHODS:
            if isinstance(obj, Conversation):
                return request.user in obj.participants.all()
            if isinstance(obj, Message):
                return obj.conversation.participants.filter(id=request.user.id).exists()
            return False
        
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            if isinstance(obj, Conversation):
                return request.user in obj.participants.all()
            if isinstance(obj, Message):
                return obj.conversation.participants.filter(id=request.user.id).exists()
            return False
        
        if request.method == 'POST':
            if isinstance(obj, Conversation):
                return request.user in obj.participants.all()
            if isinstance(obj, Message):
                return obj.conversation.participants.filter(id=request.user.id).exists()
            return False
        
        return False