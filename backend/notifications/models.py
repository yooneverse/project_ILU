from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Notification(models.Model):
    SYSTEM = 'SYSTEM'
    SURVEY = 'SURVEY'
    REVIEW = 'REVIEW'

    TYPE_CHOICES = [
        (SYSTEM, 'System'),
        (SURVEY, 'Survey'),
        (REVIEW, 'Review'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default=SYSTEM
    )
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
