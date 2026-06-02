from django.db import models
from django.conf import settings

# Типы уведомлений
NOTIFICATION_TYPES = [
    ('comment', 'Новый комментарий'),
    ('update', 'Изменение проекта'),
    ('deadline', 'Истечение срока'),
    ('mention', 'Упоминание'),
]

# Частоты сводок
DIGEST_FREQUENCIES = [
    ('instant', 'Мгновенно'),
    ('daily', 'Раз в день'),
    ('weekly', 'Раз в неделю'),
]


class Notification(models.Model):

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    link = models.CharField(max_length=500, blank=True)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='actions')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} -> {self.recipient.username}"


class NotificationPreference(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='preferences')
    push_enabled = models.BooleanField(default=True)
    email_enabled = models.BooleanField(default=True)
    quiet_hours_start = models.TimeField(null=True, blank=True)
    quiet_hours_end = models.TimeField(null=True, blank=True)
    event_filters = models.JSONField(default=dict)
    digest_frequency = models.CharField(max_length=10, choices=DIGEST_FREQUENCIES, default='instant')

    def __str__(self):
        return f"Настройки {self.user.username}"