# Django-signals_orm-0x04/messaging/views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect

@login_required
def delete_user(request):
    """View to allow a user to delete their account."""
    if request.method == 'POST':
        user = request.user
        user.delete()  # Triggers post_delete signal
        return HttpResponse("Account deleted successfully.")
    return redirect('home')  # Redirect to a home page (update URL config if needed)