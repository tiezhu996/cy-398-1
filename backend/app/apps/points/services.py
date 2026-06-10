from django.db import transaction
from app.constants.points import POINT_REASONS, SELLER_CREDIT_BASE, SELLER_CREDIT_PER_TRADE, SELLER_CREDIT_MAX
from app.apps.points.models import PointLedger
from app.apps.users.models import UserPointAccount, SellerCredit
from app.utils.logger import logger


class PointGrantService:
    @staticmethod
    @transaction.atomic
    def grant_points(user_id, order_id, points, reason_code):
        if points <= 0:
            raise ValueError("积分数量必须大于0")
        if reason_code not in POINT_REASONS:
            raise ValueError(f"无效的积分原因: {reason_code}")

        account, created = UserPointAccount.objects.select_for_update().get_or_create(
            user_id=user_id,
            defaults={"balance": 0, "total_earned": 0, "total_spent": 0},
        )
        account.balance += points
        account.total_earned += points
        account.save()

        ledger = PointLedger.objects.create(
            user_id=user_id,
            order_id=order_id,
            points=points,
            reason=reason_code,
        )

        logger.info(
            f"积分发放成功: user_id={user_id}, order_id={order_id}, "
            f"points={points}, reason={reason_code}, balance={account.balance}"
        )

        return ledger

    @staticmethod
    @transaction.atomic
    def grant_eco_trade_points(order_id, buyer_id, seller_id, items):
        from app.utils.points import calculate_points

        total_buyer_points = 0
        total_seller_points = 0

        for item in items:
            category = item.get("category", "books")
            weight_kg = float(item.get("weight_kg", 1))
            quantity = int(item.get("quantity", 1))
            item_points = calculate_points(category, weight_kg) * quantity
            total_buyer_points += item_points
            total_seller_points += item_points

        buyer_ledger = PointGrantService.grant_points(
            user_id=buyer_id,
            order_id=order_id,
            points=total_buyer_points,
            reason_code="ECO_TRADE_BUYER",
        )

        seller_ledger = PointGrantService.grant_points(
            user_id=seller_id,
            order_id=order_id,
            points=total_seller_points,
            reason_code="ECO_TRADE_SELLER",
        )

        logger.info(
            f"环保交易积分发放完成: order_id={order_id}, "
            f"buyer_id={buyer_id}, buyer_points={total_buyer_points}, "
            f"seller_id={seller_id}, seller_points={total_seller_points}"
        )

        return {
            "buyer_ledger": buyer_ledger,
            "seller_ledger": seller_ledger,
            "buyer_points": total_buyer_points,
            "seller_points": total_seller_points,
        }


class SellerCreditService:
    @staticmethod
    @transaction.atomic
    def refresh_seller_credit(seller_id, earned_points=0):
        credit, created = SellerCredit.objects.select_for_update().get_or_create(
            seller_id=seller_id,
            defaults={
                "credit_score": SELLER_CREDIT_BASE,
                "trade_count": 0,
                "total_points_earned": 0,
            },
        )

        credit.trade_count += 1
        credit.total_points_earned += earned_points
        credit.credit_score = min(
            SELLER_CREDIT_BASE + credit.trade_count * SELLER_CREDIT_PER_TRADE,
            SELLER_CREDIT_MAX,
        )
        credit.save()

        logger.info(
            f"卖家信用刷新: seller_id={seller_id}, "
            f"credit_score={credit.credit_score}, "
            f"trade_count={credit.trade_count}"
        )

        return credit
