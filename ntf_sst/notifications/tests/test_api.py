from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Notification

User = get_user_model()


class APITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_get_notifications(self):
        response = self.client.get('/api/notifications/')
        self.assertEqual(response.status_code, 200)

    def test_mark_as_read(self):
        notif = Notification.objects.create(
            recipient=self.user,
            notification_type='update',
            title='Тест',
            message='Сообщение',
            link='/'
        )
        response = self.client.post(f'/api/notifications/{notif.id}/mark_read/')
        self.assertEqual(response.status_code, 200)
        notif.refresh_from_db()
        self.assertTrue(notif.is_read)

    def test_mark_invalid_id(self):
        response = self.client.post('/api/notifications/99999/mark_read/')
        self.assertEqual(response.status_code, 404)