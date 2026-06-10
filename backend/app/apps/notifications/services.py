from app.apps.notifications.models import Notification
from app.utils.logger import logger


class NotificationService:
    @staticmethod
    def send_notification(user_id, title, content):
        notification = Notification.objects.create(
            user_id=user_id,
            title=title,
            content=content,
        )
        logger.info(f"通知推送成功: user_id={user_id}, title={title}")
        return notification

    @staticmethod
    def send_eco_points_notification(user_id, points, reason, order_id, role):
        role_text = "买家" if role == "buyer" else "卖家"
        title = f"环保积分到账 +{points}"
        content = (
            f"您作为{role_text}完成了一笔环保交易（订单号：{order_id}），"
            f"获得 {points} 环保积分。{reason}"
        )
        return NotificationService.send_notification(user_id, title, content)

    @staticmethod
    def send_seller_credit_notification(seller_id, credit_score, trade_count):
        title = "卖家信用已更新"
        content = (
            f"您的卖家信用已更新，当前信用分为 {credit_score} 分，"
            f"累计完成交易 {trade_count} 笔。"
        )
        return NotificationService.send_notification(seller_id, title, content)
