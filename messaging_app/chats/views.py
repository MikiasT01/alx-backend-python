# messaging_app/chats/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend  # Added for filters
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for listing and creating conversations."""
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [DjangoFilterBackend]  # Added filter backend
    filterset_fields = ['conversation_id', 'participants__user_id']  # Allow filtering by conversation_id and participant user_id

    def create(self, request, *args, **kwargs):
        """Create a new conversation with participants."""
        participants = request.data.get('participants', [])
        if not participants or len(participants) < 2:
            return Response(
                {"error": "A conversation must have at least two participants."},
                status=status.HTTP_400_BAD_REQUEST
            )
        users = User.objects.filter(user_id__in=participants)
        if len(users) != len(participants):
            return Response(
                {"error": "One or more participant IDs are invalid."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(context={'participants': users})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        """List all conversations with nested data."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for sending messages to an existing conversation."""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend]  # Added filter backend
    filterset_fields = ['message_id', 'conversation__conversation_id', 'sender__user_id']  # Allow filtering by message_id, conversation_id, and sender user_id

    def create(self, request, *args, **kwargs):
        """Send a message to an existing conversation."""
        conversation_id = request.data.get('conversation')
        if not conversation_id:
            return Response(
                {"error": "Conversation ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        request.data['conversation'] = conversation.id  # Set the internal ID for the serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        """List all messages (optionally filter by conversation)."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)