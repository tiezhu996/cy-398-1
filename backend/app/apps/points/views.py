from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from app.utils.points import calculate_points
from app.apps.points.queries import PointQueryService, SellerCreditQueryService
from app.constants.errors import ERRORS
from app.utils.logger import logger


class PointViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["get"])
    def summary(self, request):
        user_id = request.query_params.get("user_id")
        if not user_id:
            raise APIException(
                detail=ERRORS.get("VALIDATION_FAILED"),
                code="VALIDATION_FAILED",
            )

        account = PointQueryService.get_user_point_account(int(user_id))
        return Response({
            "user_id": account["user_id"],
            "available_points": account["balance"],
            "total_earned": account["total_earned"],
            "total_spent": account["total_spent"],
            "coupons": [{"name": "循环减免券", "cost": 100}],
        })

    @action(detail=False, methods=["get"])
    def ledger(self, request):
        user_id = request.query_params.get("user_id")
        if not user_id:
            raise APIException(
                detail=ERRORS.get("VALIDATION_FAILED"),
                code="VALIDATION_FAILED",
            )

        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 20))
        reason = request.query_params.get("reason")

        result = PointQueryService.get_point_ledger(
            user_id=int(user_id),
            page=page,
            page_size=page_size,
            reason=reason,
        )
        return Response(result)

    @action(detail=False, methods=["post"])
    def calculate(self, request):
        category = request.data.get("category", "books")
        weight_kg = float(request.data.get("weight_kg", 1))
        points = calculate_points(category, weight_kg)
        logger.info(f"积分计算: category={category}, weight_kg={weight_kg}, points={points}")
        return Response({"points": points})


class SellerCreditViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["get"])
    def info(self, request):
        seller_id = request.query_params.get("seller_id")
        if not seller_id:
            raise APIException(
                detail=ERRORS.get("VALIDATION_FAILED"),
                code="VALIDATION_FAILED",
            )

        credit = SellerCreditQueryService.get_seller_credit(int(seller_id))
        return Response(credit)
