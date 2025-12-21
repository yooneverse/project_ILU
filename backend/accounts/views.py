# accounts/views.py
from rest_framework.decorators import api_view, permission_classes, authentication_classes
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


# ✅ 아이디 중복 확인 - 인증 완전 우회
@api_view(['GET'])
@authentication_classes([])  # 인증 클래스 비활성화
@permission_classes([AllowAny])  # 권한 체크 비활성화
def check_username(request, username):
    """
    아이디 중복 확인
    - 존재하면 409 Conflict
    - 존재하지 않으면 200 OK
    """
    print(f"[CHECK_USERNAME] Called with username: {username}")
    
    try:
        # 아이디가 이미 존재하는지 확인
        exists = User.objects.filter(username=username).exists()
        print(f"[CHECK_USERNAME] Username exists: {exists}")
        
        if exists:
            return Response(
                {'message': '이미 사용 중인 아이디입니다.'},
                status=status.HTTP_409_CONFLICT
            )
        
        # 사용 가능한 아이디
        return Response(
            {'message': '사용 가능한 아이디입니다.'},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        # 에러 로깅
        print(f"[CHECK_USERNAME ERROR] {e}")
        return Response(
            {'message': '중복 확인 중 오류가 발생했습니다.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ✅ 회원가입 - 인증 완전 우회
@api_view(['POST'])
@authentication_classes([])  # 인증 클래스 비활성화
@permission_classes([AllowAny])  # 권한 체크 비활성화
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