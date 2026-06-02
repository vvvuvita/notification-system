from rest_framework import serializers
from .models import Notification, NotificationPreference


class NotificationSerializer(serializers.ModelSerializer):

    recipient_name = serializers.CharField(source='recipient.username', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'link', 'notification_type',
                  'is_read', 'created_at', 'recipient_name']


class NotificationPreferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = NotificationPreference
        fields = ['push_enabled', 'email_enabled', 'quiet_hours_start',
                  'quiet_hours_end', 'digest_frequency']