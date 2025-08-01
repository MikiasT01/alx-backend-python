# Django-signals_orm-0x04/messaging/views.py
from django.shortcuts import render
from .models import Message, MessageHistory

def message_history(request, message_id):
    message = Message.objects.get(id=message_id)
    history = MessageHistory.objects.filter(message=message).order_by('edited_at')
    return render(request, 'messaging/history.html', {'message': message, 'history': history})