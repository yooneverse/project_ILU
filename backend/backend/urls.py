from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 이 부분 추가! (404 해결)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # 기존 코드 유지
    path('accounts/', include('accounts.urls')),
    path('notifications/', include('notifications.urls')),
    path('api/v1/users/', include('users.urls')),
]