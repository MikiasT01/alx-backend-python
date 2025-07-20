# messaging_app/chats/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter  # Explicitly import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

router = DefaultRouter()  # Initialize DefaultRouter
router.register(r'conversations', ConversationViewSet)  # Register ConversationViewSet
router.register(r'messages', MessageViewSet)  # Register MessageViewSet

urlpatterns = [
    path('', include(router.urls)),  # Include the router's URL patterns
]