from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from app.apps.products.models import Product
from app.apps.products.serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params
        if category := params.get("category"):
            qs = qs.filter(category=category)
        if condition := params.get("condition"):
            qs = qs.filter(condition=condition)
        if min_price := params.get("min_price"):
            qs = qs.filter(sale_price__gte=min_price)
        if max_price := params.get("max_price"):
            qs = qs.filter(sale_price__lte=max_price)
        if keyword := params.get("keyword"):
            vector = SearchVector("name", weight="A") + SearchVector("description", weight="B")
            query = SearchQuery(keyword)
            qs = qs.annotate(rank=SearchRank(vector, query)).filter(rank__gt=0).order_by("-rank")
        sort = params.get("sort")
        if sort == "price":
            qs = qs.order_by("sale_price")
        elif sort == "newest":
            qs = qs.order_by("-created_at")
        return qs

class StatsViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["get"])
    def trades(self, request):
        return Response({"range": request.query_params.get("range", "day"), "trade_count": 38, "trade_amount": 12680, "hot_categories": [{"category": "books", "count": 16}], "active_users": 72})
