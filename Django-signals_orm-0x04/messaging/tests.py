# Django-signals_orm-0x04/messaging/tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache
from .models import Message

class CacheTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='testpass123')
        self.user2 = User.objects.create_user(username='user2', password='testpass123')
        self.parent = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Parent message'
        )
        self.client.login(username='user1', password='testpass123')
        cache.clear()  # Clear cache before tests

    def test_threaded_conversation_caching(self):
        """Test that threaded_conversation view is cached for 60 seconds."""
        with self.assertNumQueries(1):  # First request should hit the database
            response1 = self.client.get(reverse('threaded_conversation', args=[self.parent.id]))
        self.assertEqual(response1.status_code, 200)
        self.assertContains(response1, 'Parent message')

        with self.assertNumQueries(0):  # Second request should use cache
            response2 = self.client.get(reverse('threaded_conversation', args=[self.parent.id]))
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, 'Parent message')