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


# ✅ 그라데이션 API용 import
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import re


# ✅ 큐레이션 카드 그라데이션 생성 API
@csrf_exempt
def generate_gradient(request):
    """
    큐레이션 카드 그라데이션 생성 API
    
    POST /api/surveys/generate-gradient/
    Body: {
        "typeName": "중재자",
        "score": 18
    }
    
    Response: {
        "gradient": "linear-gradient(135deg, #10b981 0%, #059669 100%)"
    }
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        # Request 데이터 파싱
        data = json.loads(request.body)
        type_name = data.get('typeName')
        score = data.get('score')
        
        if not type_name or score is None:
            return JsonResponse({
                'error': 'typeName and score are required'
            }, status=400)
        
        print(f"[Gradient API] Generating for {type_name} (score: {score})")
        
        # GMS API 호출
        gms_response = requests.post(
            'https://gms.ssafy.io/gmsapi/api.openai.com/v1/chat/completions',
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer S14P02EA06-c48c4cbb-7e8b-4623-a77d-2f14e4f0025e'
            },
            json={
                'model': 'gpt-4o',
                'messages': [
                    {
                        'role': 'system',
                        'content': 'You are a color expert. Generate beautiful CSS gradient colors based on personality types and scores. Return ONLY the CSS gradient code without any explanation or markdown.'
                    },
                    {
                        'role': 'user',
                        'content': f'Create a CSS linear-gradient for "{type_name}" personality with score {score}/50. Higher scores = more vibrant colors. Format: linear-gradient(135deg, #COLOR1 0%, #COLOR2 100%). Return ONLY the gradient code.'
                    }
                ],
                'temperature': 0.7,
                'max_tokens': 100
            },
            timeout=10
        )
        
        print(f"[Gradient API] GMS status: {gms_response.status_code}")
        
        if gms_response.status_code != 200:
            print(f"[Gradient API] GMS error: {gms_response.text}")
            return get_default_gradient_response(type_name)
        
        result = gms_response.json()
        
        if result.get('choices') and len(result['choices']) > 0:
            gradient = result['choices'][0]['message']['content'].strip()
            
            # 마크다운 코드 블록 제거
            gradient = re.sub(r'```css\n?', '', gradient)
            gradient = re.sub(r'```\n?', '', gradient)
            gradient = gradient.replace('`', '').strip()
            
            print(f"[Gradient API] ✅ Generated: {gradient}")
            
            if 'linear-gradient' in gradient:
                return JsonResponse({'gradient': gradient})
            else:
                return get_default_gradient_response(type_name)
        
        return get_default_gradient_response(type_name)
        
    except requests.exceptions.RequestException as e:
        print(f"[Gradient API] Request error: {str(e)}")
        return get_default_gradient_response(type_name)
    except Exception as e:
        print(f"[Gradient API] Error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


def get_default_gradient_response(type_name):
    """API 실패 시 기본 그라데이션 반환"""
    DEFAULT_GRADIENTS = {
        '수호자': 'linear-gradient(135deg, #3b82f6 0%, #1e40af 100%)',
        '개척자': 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
        '조율자': 'linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%)',
        '중재자': 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
        '연구자': 'linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)',
        '기술자': 'linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)',
        '혁신가': 'linear-gradient(135deg, #ec4899 0%, #be185d 100%)',
        '공감자': 'linear-gradient(135deg, #14b8a6 0%, #0d9488 100%)'
    }
    
    gradient = DEFAULT_GRADIENTS.get(
        type_name,
        'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    )
    
    print(f"[Gradient API] Using default: {gradient}")
    return JsonResponse({'gradient': gradient})