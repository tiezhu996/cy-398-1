from django.db import models

class PointLedger(models.Model):
    user_id = models.BigIntegerField()
    order_id = models.BigIntegerField()
    points = models.IntegerField()
    reason = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
