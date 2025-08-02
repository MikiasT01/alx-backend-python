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
    message = (Message.objects.select_related('sender', 'receiver')
               .prefetch_related('replies__sender', 'replies__receiver')
               .get(id=message_id))
    def get_all_replies(parent_id):
        replies = (Message.objects.filter(parent_message_id=parent_id)
                   .select_related('sender', 'receiver')
                   .prefetch_related('replies__sender', 'replies__receiver'))
        all_replies = list(replies)
        for reply in replies:
            all_replies.extend(get_all_replies(reply.id))
        return all_replies
    replies = get_all_replies(message_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                sender=request.user,
                receiver=message.receiver,
                content=content,
                parent_message=message
            )
            return redirect('threaded_conversation', message_id=message_id)
    return render(request, 'messaging/threaded.html', {'message': message, 'replies': replies})

@login_required
def inbox(request):
    """Display only unread messages for the logged-in user with optimized fields."""
    unread_messages = Message.unread.unread_for_user(request.user)  # Explicitly use the custom manager
    return render(request, 'messaging/inbox.html', {'unread_messages': unread_messages})