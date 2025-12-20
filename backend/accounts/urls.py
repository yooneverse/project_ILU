# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('me/', views.me, name='user-me'),
    path('signup/', views.signup, name='signup'),  # ✅ 추가
]