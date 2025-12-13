from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from notifications.models import Notification


class SurveyStartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        Notification.objects.get_or_create(
            user=request.user,
            type=Notification.SURVEY,
            is_read=False,
            defaults={
                'message': '아직 설문이 완료되지 않았어요. 이어서 진행해 주세요.'
            }
        )

        return Response({'status': 'survey started'})
    
class SurveyCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        Notification.objects.filter(
            user=request.user,
            type=Notification.SURVEY,
            is_read=False
        ).update(is_read=True)

        return Response({'status': 'survey completed'})
