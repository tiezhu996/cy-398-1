from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from app.apps.orders.models import CartItem, Order
from app.apps.orders.serializers import CartItemSerializer, OrderSerializer
from app.apps.products.models import Product
from app.apps.points.services import PointGrantService, SellerCreditService
from app.apps.notifications.services import NotificationService
from app.constants.enums import ORDER_STATUS
from app.constants.errors import ERRORS
from app.utils.logger import logger


class CartViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderSerializer

    @action(detail=False, methods=["post"])
    def checkout(self, request):
        buyer_id = request.data.get("buyer_id")
        items = list(CartItem.objects.filter(user_id=buyer_id).values("product_id", "quantity"))
        order = Order.objects.create(buyer_id=buyer_id, items=items, total_amount=max(len(items), 1) * 49)
        CartItem.objects.filter(user_id=buyer_id).delete()
        return Response(OrderSerializer(order).data)

    @action(detail=True, methods=["patch"])
    def status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get("status")

        if new_status and new_status not in ORDER_STATUS:
            raise APIException(
                detail=ERRORS.get("ORDER_STATUS_INVALID"),
                code="ORDER_STATUS_INVALID",
            )

        old_status = order.status
        order.status = new_status or order.status
        order.save(update_fields=["status"])

        if old_status != "received" and new_status == "received":
            try:
                self._process_eco_points(order)
            except Exception as e:
                logger.error(f"确认收货发放积分失败: order_id={order.id}, error={str(e)}")

        return Response(OrderSerializer(order).data)

    def _process_eco_points(self, order):
        items_with_detail = self._enrich_order_items(order.items)

        seller_id = items_with_detail[0]["seller_id"] if items_with_detail else None
        if not seller_id:
            logger.warning(f"订单无有效商品，跳过积分发放: order_id={order.id}")
            return

        result = PointGrantService.grant_eco_trade_points(
            order_id=order.id,
            buyer_id=order.buyer_id,
            seller_id=seller_id,
            items=items_with_detail,
        )

        credit = SellerCreditService.refresh_seller_credit(
            seller_id=seller_id,
            earned_points=result["seller_points"],
        )

        NotificationService.send_eco_points_notification(
            user_id=order.buyer_id,
            points=result["buyer_points"],
            reason="感谢您支持环保循环消费",
            order_id=order.id,
            role="buyer",
        )

        NotificationService.send_eco_points_notification(
            user_id=seller_id,
            points=result["seller_points"],
            reason="您的商品为环保事业做出了贡献",
            order_id=order.id,
            role="seller",
        )

        NotificationService.send_seller_credit_notification(
            seller_id=seller_id,
            credit_score=credit.credit_score,
            trade_count=credit.trade_count,
        )

        logger.info(
            f"确认收货积分发放完成: order_id={order.id}, "
            f"buyer_id={order.buyer_id}, seller_id={seller_id}"
        )

    def _enrich_order_items(self, items):
        product_ids = [item["product_id"] for item in items]
        products = Product.objects.filter(id__in=product_ids)
        product_map = {p.id: p for p in products}

        enriched = []
        for item in items:
            product = product_map.get(item["product_id"])
            if product:
                enriched.append({
                    "product_id": item["product_id"],
                    "quantity": item.get("quantity", 1),
                    "category": product.category,
                    "weight_kg": product.weight_kg,
                    "seller_id": product.seller_id,
                    "name": product.name,
                })
        return enriched
