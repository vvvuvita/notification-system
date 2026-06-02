from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Notification, NotificationPreference
from ..tasks import send_notification_to_user

User = get_user_model()


class TasksTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.prefs = NotificationPreference.objects.create(user=self.user)

    def test_task_does_not_crash(self):
        notif = Notification.objects.create(
            recipient=self.user,
            notification_type='update',
            title='Тест',
            message='Сообщение'
        )
        result = send_notification_to_user.delay(notif.id, self.user.id)
        self.assertIsNotNone(result)