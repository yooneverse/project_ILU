# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('me/', views.me, name='user-me'),
    path('check-username/<str:username>/', views.check_username, name='check-username'),  # ✅ 추가
    path('signup/', views.signup, name='signup'),
]