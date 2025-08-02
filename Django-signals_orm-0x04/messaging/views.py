# Django-signals_orm-0x04/messaging/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Message

@login_required
def message_history(request, message_id):
    message = Message.objects.get(id=message_id)
    history = MessageHistory.objects.filter(message=message).order_by('edited_at')
    return render(request, 'messaging/history.html', {'message': message, 'history': history})

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return HttpResponse("Account deleted successfully.")
    return redirect('home')

@login_required
def threaded_conversation(request, message_id):
    """Display a message and all its threaded replies efficiently."""
    # Optimize query with select_related for foreign keys and prefetch_related for replies
    message = (Message.objects.select_related('sender', 'receiver')
               .prefetch_related('replies__sender', 'replies__receiver')
               .get(id=message_id))

    # Recursive query using filter to fetch all replies
    def get_all_replies(parent_id):
        replies = (Message.objects.filter(parent_message_id=parent_id)
                   .select_related('sender', 'receiver')
                   .prefetch_related('replies__sender', 'replies__receiver'))
        all_replies = list(replies)
        for reply in replies:
            all_replies.extend(get_all_replies(reply.id))
        return all_replies

    replies = get_all_replies(message_id)
    
    # Allow adding a reply (associating sender with request.user)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                sender=request.user,
                receiver=message.receiver,  # Keep receiver as the original recipient
                content=content,
                parent_message=message
            )
            return redirect('threaded_conversation', message_id=message_id)

    return render(request, 'messaging/threaded.html', {'message': message, 'replies': replies})