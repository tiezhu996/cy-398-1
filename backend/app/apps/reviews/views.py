from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from app.apps.reviews.models import Review
from app.apps.reviews.serializers import ReviewSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    @action(detail=False, methods=["get"])
    def credit(self, request):
        user_id = request.query_params.get("user_id")
        ratings = Review.objects.filter(reviewee_id=user_id).values_list("rating", flat=True)
        total = len(ratings)
        positive = len([score for score in ratings if score >= 4])
        rate = positive / total if total else 1
        return Response({"user_id": user_id, "positive_rate": rate, "credit_level": "A" if rate >= 0.9 else "B"})
