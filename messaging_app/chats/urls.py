# messaging_app/chats/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter  # Added DefaultRouter
from .views import ConversationViewSet, MessageViewSet

router = DefaultRouter()  # Initialize the router
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Include router URLs
]