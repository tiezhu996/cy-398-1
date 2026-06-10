from django.urls import include, path
from rest_framework.routers import DefaultRouter
from app.apps.products.views import ProductViewSet, StatsViewSet
from app.apps.orders.views import CartViewSet, OrderViewSet
from app.apps.points.views import PointViewSet, SellerCreditViewSet
from app.apps.reviews.views import ReviewViewSet
from app.apps.notifications.views import NotificationViewSet

router = DefaultRouter()
router.register("products", ProductViewSet, basename="products")
router.register("orders/cart", CartViewSet, basename="cart")
router.register("orders", OrderViewSet, basename="orders")
router.register("points", PointViewSet, basename="points")
router.register("seller-credit", SellerCreditViewSet, basename="seller-credit")
router.register("reviews", ReviewViewSet, basename="reviews")
router.register("notifications", NotificationViewSet, basename="notifications")
router.register("stats", StatsViewSet, basename="stats")

urlpatterns = [path("api/", include(router.urls))]
