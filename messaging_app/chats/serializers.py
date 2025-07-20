# messaging_app/chats/serializers.py
from rest_framework import serializers
from rest_framework.exceptions import ValidationError  # Added for ValidationError
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model with sender details."""
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']

    def validate_message_body(self, value):
        """Validate that message_body is not empty."""
        if not value.strip():
            raise ValidationError("Message body cannot be empty or whitespace.")
        return value

class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation model with nested messages and participants."""
    messages = MessageSerializer(many=True, read_only=True)
    participants = UserSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()  # Custom field using SerializerMethodField

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at', 'message_count']

    def get_message_count(self, obj):
        """Return the number of messages in the conversation."""
        return obj.messages.count()

    def validate(self, data):
        """Custom validation to ensure at least two participants."""
        if 'participants' not in self.context or len(self.context['participants']) < 2:
            raise ValidationError("A conversation must have at least two participants.")
        return data

    def create(self, validated_data):
        """Custom create method to handle nested participants."""
        participants_data = self.context.get('participants', [])
        conversation = Conversation.objects.create()
        conversation.participants.set(participants_data)
        return conversation