# Django-signals_orm-0x04/messaging/managers.py
from django.db import models

class UnreadMessagesManager(models.Manager):
    """Custom manager to filter unread messages for a specific user."""
    def unread_for_user(self, user):
        return self.filter(receiver=user, read=False).only('id', 'content', 'sender', 'timestamp')