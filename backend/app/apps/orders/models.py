from django.db import models

class CartItem(models.Model):
    user_id = models.BigIntegerField()
    product_id = models.BigIntegerField()
    quantity = models.PositiveIntegerField(default=1)

class Order(models.Model):
    buyer_id = models.BigIntegerField()
    status = models.CharField(max_length=32, default="pending_pay")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    items = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
