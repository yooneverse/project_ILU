# accounts/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    """현재 로그인한 사용자 정보"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


# ✅ 추가: 회원가입 엔드포인트
@api_view(['POST'])
@permission_classes([AllowAny])  # 인증 불필요
def signup(request):
    """회원가입"""
    try:
        # 필수 필드 확인
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        first_name = request.data.get('first_name', '')
        
        # 유효성 검사
        if not username:
            return Response(
                {'username': ['아이디는 필수입니다.']},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not password:
            return Response(
                {'password': ['비밀번호는 필수입니다.']},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not email:
            return Response(
                {'email': ['이메일은 필수입니다.']},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 아이디 중복 확인
        if User.objects.filter(username=username).exists():
            return Response(
                {'username': ['이미 사용 중인 아이디입니다.']},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 이메일 중복 확인
        if User.objects.filter(email=email).exists():
            return Response(
                {'email': ['이미 사용 중인 이메일입니다.']},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 사용자 생성
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name
        )
        
        # 응답
        serializer = UserSerializer(user)
        return Response(
            {
                'message': '회원가입이 완료되었습니다.',
                'user': serializer.data
            },
            status=status.HTTP_201_CREATED
        )
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )