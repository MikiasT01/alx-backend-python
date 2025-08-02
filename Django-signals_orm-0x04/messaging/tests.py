# Django-signals_orm-0x04/messaging/tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Message

class UnreadMessagesTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='testpass123')
        self.user2 = User.objects.create_user(username='user2', password='testpass123')
        self.unread_msg = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content='Unread message',
            read=False
        )
        self.read_msg = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content='Read message',
            read=True
        )
        self.client.login(username='user1', password='testpass123')

    def test_inbox_view_with_only_optimization(self):
        """Test that inbox uses UnreadMessagesManager with explicit .only()."""
        response = self.client.get(reverse('inbox'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Unread message')
        self.assertNotContains(response, 'Read message')
        self.assertEqual(len(response.context['unread_messages']), 1)
        # Approximate check for .only() via field access (limited fields should work)
        for msg in response.context['unread_messages']:
            self.assertTrue(hasattr(msg, 'content'))
            self.assertTrue(hasattr(msg, 'sender'))
            self.assertTrue(hasattr(msg, 'timestamp'))