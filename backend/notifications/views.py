from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Notification.objects.filter(user=request.user)
        serializer = NotificationSerializer(qs, many=True)

        return Response({
            'notifications': serializer.data,
            'unread_count': qs.filter(is_read=False).count()
        })


class NotificationReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        notification = Notification.objects.get(
            pk=pk,
            user=request.user
        )
        notification.is_read = True
        notification.save()

        return Response({'status': 'ok'})
