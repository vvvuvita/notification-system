from celery import shared_task
from .models import Notification, NotificationPreference
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_notification_to_user(notification_id, user_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        try:
            prefs = NotificationPreference.objects.get(user_id=user_id)
        except NotificationPreference.DoesNotExist:
            logger.warning(f"Нет настроек у user {user_id}")
            return

        if prefs.email_enabled:
            send_email_task.delay(notification.id, user_id)
            print(f"Email для {user_id} поставлен в очередь")

        if prefs.push_enabled:
            send_push_task.delay(notification.id, user_id)
            print(f"Push для {user_id} поставлен в очередь")

    except Notification.DoesNotExist:
        logger.error(f"Уведомление {notification_id} не найдено")


@shared_task
def send_email_task(notification_id, user_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        print(f"   EMAIL to user {user_id}: {notification.title}")
        print(f"   Message: {notification.message}")
        print(f"   Link: {notification.link}")
    except Exception as e:
        logger.error(f"Email error: {e}")
        raise send_email_task.retry(exc=e, countdown=60)


@shared_task
def send_push_task(notification_id, user_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        print(f"PUSH to user {user_id}: {notification.title}")
    except Exception as e:
        logger.error(f"Push error: {e}")