# Django-signals_orm-0x04/messaging/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, MessageHistory

class EditSignalTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass123')
        self.user2 = User.objects.create_user(username='user2', password='testpass123')
        self.message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Original content'
        )

    def test_message_edit_logging(self):
        self.message.content = 'Edited content'
        self.message.save()
        self.assertEqual(MessageHistory.objects.count(), 1)
        history = MessageHistory.objects.first()
        self.assertEqual(history.message, self.message)
        self.assertEqual(history.old_content, 'Original content')
        self.assertEqual(history.edited_by, self.user1)
        self.assertTrue(self.message.edited)

    def test_history_includes_timestamp(self):
        self.message.content = 'Edited content'
        self.message.save()
        history = MessageHistory.objects.first()
        self.assertIsNotNone(history.edited_at)