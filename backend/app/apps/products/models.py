from django.db import models

class Product(models.Model):
    seller_id = models.BigIntegerField()
    name = models.CharField(max_length=120)
    description = models.TextField()
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=24)
    category = models.CharField(max_length=32)
    images = models.JSONField(default=list)
    weight_kg = models.FloatField(default=1)
    is_on_sale = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
