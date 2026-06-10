from app.apps.points.models import PointLedger
from app.apps.users.models import UserPointAccount, SellerCredit
from app.constants.points import POINT_REASONS
from app.utils.logger import logger


class PointQueryService:
    @staticmethod
    def get_user_point_account(user_id):
        account, _ = UserPointAccount.objects.get_or_create(
            user_id=user_id,
            defaults={"balance": 0, "total_earned": 0, "total_spent": 0},
        )
        return {
            "user_id": account.user_id,
            "balance": account.balance,
            "total_earned": account.total_earned,
            "total_spent": account.total_spent,
            "updated_at": account.updated_at,
        }

    @staticmethod
    def get_point_ledger(user_id, page=1, page_size=20, reason=None):
        queryset = PointLedger.objects.filter(user_id=user_id).order_by("-created_at")
        if reason:
            queryset = queryset.filter(reason=reason)

        total = queryset.count()
        start = (page - 1) * page_size
        end = start + page_size
        records = queryset[start:end]

        ledger_list = []
        for record in records:
            ledger_list.append({
                "id": record.id,
                "user_id": record.user_id,
                "order_id": record.order_id,
                "points": record.points,
                "reason": record.reason,
                "reason_text": POINT_REASONS.get(record.reason, record.reason),
                "created_at": record.created_at,
            })

        logger.info(f"积分记录查询: user_id={user_id}, count={len(ledger_list)}, total={total}")

        return {
            "list": ledger_list,
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    @staticmethod
    def get_order_points(order_id):
        ledgers = PointLedger.objects.filter(order_id=order_id)
        result = []
        for ledger in ledgers:
            result.append({
                "id": ledger.id,
                "user_id": ledger.user_id,
                "points": ledger.points,
                "reason": ledger.reason,
                "reason_text": POINT_REASONS.get(ledger.reason, ledger.reason),
                "created_at": ledger.created_at,
            })
        return result


class SellerCreditQueryService:
    @staticmethod
    def get_seller_credit(seller_id):
        credit, _ = SellerCredit.objects.get_or_create(
            seller_id=seller_id,
            defaults={
                "credit_score": 100,
                "trade_count": 0,
                "total_points_earned": 0,
            },
        )
        return {
            "seller_id": credit.seller_id,
            "credit_score": credit.credit_score,
            "trade_count": credit.trade_count,
            "total_points_earned": credit.total_points_earned,
            "updated_at": credit.updated_at,
        }
