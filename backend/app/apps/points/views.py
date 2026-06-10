from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from app.utils.points import calculate_points

class PointViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["get"])
    def summary(self, request):
        user_id = request.query_params.get("user_id", "1")
        return Response({"user_id": user_id, "available_points": 256, "coupons": [{"name": "循环减免券", "cost": 100}]})

    @action(detail=False, methods=["post"])
    def calculate(self, request):
        return Response({"points": calculate_points(request.data.get("category", "books"), float(request.data.get("weight_kg", 1)))})
