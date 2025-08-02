# Django-signals_orm-0x04/messaging/tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

class DeleteSignalTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='testpass123')
        self.user2 = User.objects.create_user(username='user2', password='testpass123')
        self.message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Test message'
        )
        Notification.objects.create(user=self.user2, message=self.message)
        MessageHistory.objects.create(
            message=self.message,
            old_content='Original',
            edited_by=self.user1
        )
        self.client.login(username='user1', password='testpass123')

    def test_user_deletion_cleans_up_data(self):
        """Test that deleting a user cleans up related data with filter-based deletion."""
        initial_message_count = Message.objects.count()
        initial_notification_count = Notification.objects.count()
        initial_history_count = MessageHistory.objects.count()
        self.client.post('/delete/')
        self.assertEqual(User.objects.filter(username='user1').count(), 0)
        self.assertEqual(Message.objects.count(), initial_message_count - 2)  # Adjust for related deletions
        self.assertEqual(Notification.objects.count(), initial_notification_count - 1)
        self.assertEqual(MessageHistory.objects.count(), initial_history_count - 1)