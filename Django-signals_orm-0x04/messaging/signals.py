# Django-signals_orm-0x04/messaging/signals.py
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """Create a notification when a new message is saved."""
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """Log the old content of a message before it’s updated."""
    if instance.pk:  # Check if the instance already exists (i.e., being updated)
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content and not old_message.edited:
                MessageHistory.objects.create(message=instance, old_content=old_message.content)
                instance.edited = True
        except Message.DoesNotExist:
            pass  # Handle case where instance might not be fully initialized