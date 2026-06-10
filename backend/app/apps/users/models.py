from django.db import models


class UserPointAccount(models.Model):
    user_id = models.BigIntegerField(unique=True)
    balance = models.IntegerField(default=0)
    total_earned = models.IntegerField(default=0)
    total_spent = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_point_account"


class SellerCredit(models.Model):
    seller_id = models.BigIntegerField(unique=True)
    credit_score = models.IntegerField(default=100)
    trade_count = models.IntegerField(default=0)
    total_points_earned = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "seller_credit"
