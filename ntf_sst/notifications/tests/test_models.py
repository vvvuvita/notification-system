from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Notification

User = get_user_model()


class NotificationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_create_notification(self):
        notif = Notification.objects.create(
            recipient=self.user,
            notification_type='update',
            title='Тест',
            message='Сообщение',
            link='/test/'
        )
        self.assertEqual(notif.title, 'Тест')
        self.assertFalse(notif.is_read)