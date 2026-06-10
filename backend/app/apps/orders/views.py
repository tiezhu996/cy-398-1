from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from app.apps.orders.models import CartItem, Order
from app.apps.orders.serializers import CartItemSerializer, OrderSerializer

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
        order.status = request.data.get("status", order.status)
        order.save(update_fields=["status"])
        return Response(OrderSerializer(order).data)
