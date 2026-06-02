from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .models import Notification, NotificationPreference
from .serializers import NotificationSerializer, NotificationPreferenceSerializer
from .tasks import send_notification_to_user

User = get_user_model()

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'read'})

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        self.get_queryset().update(is_read=True)
        return Response({'status': 'all_read'})


class PreferenceViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        prefs, created = NotificationPreference.objects.get_or_create(user=request.user)
        serializer = NotificationPreferenceSerializer(prefs)
        return Response(serializer.data)

    def update(self, request):
        prefs, created = NotificationPreference.objects.get_or_create(user=request.user)
        serializer = NotificationPreferenceSerializer(prefs, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def test_notification(request):

    user = User.objects.first()
    if not user:
        return JsonResponse(
            {'error': 'Нет пользователей в базе данных'})

    notif = Notification.objects.create(
        recipient=user,
        notification_type=Notification.Type.UPDATE,
        title="Тестовое уведомление",
        message="Это проверка системы уведомлений",
        link="/admin/"
    )

    send_notification_to_user.delay(notif.id, user.id)

    return JsonResponse({
        'status': 'ok',
        'notification_id': notif.id,
        'message': f'Уведомление отправлено пользователю {user.username}',
        'user_email': user.email
    })