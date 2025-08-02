# Django-signals_orm-0x04/messaging/views.py
from django.shortcuts import render
from .models import Message

def threaded_conversation(request, message_id):
    """Display a message and all its threaded replies efficiently."""
    # Use select_related for foreign key optimizations (sender, receiver)
    # Use prefetch_related for reverse relation (replies)
    message = Message.objects.select_related('sender', 'receiver').prefetch_related('replies').get(id=message_id)
    
    # Recursive function to get all replies (including nested replies)
    def get_all_replies(message):
        replies = message.replies.all().select_related('sender', 'receiver').prefetch_related('replies')
        all_replies = []
        for reply in replies:
            all_replies.append(reply)
            all_replies.extend(get_all_replies(reply))
        return all_replies

    replies = get_all_replies(message)
    return render(request, 'messaging/threaded.html', {'message': message, 'replies': replies})