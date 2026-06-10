from django.db import models

class Review(models.Model):
    order_id = models.BigIntegerField()
    reviewer_id = models.BigIntegerField()
    reviewee_id = models.BigIntegerField()
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
