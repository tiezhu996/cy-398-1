from django.db import models

class Notification(models.Model):
    user_id = models.BigIntegerField()
    title = models.CharField(max_length=120)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
