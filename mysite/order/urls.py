from django.urls import path, include

from order.views import OrderViewSet, OrderItemViewSet

from rest_framework.routers import DefaultRouter

app_name = "order"

routers = DefaultRouter()

from django.urls import path, include

routers.register("order", OrderViewSet, basename="order")

urlpatterns = [
    path("order", include(routers.urls)),
    path("orders", OrderItemViewSet.as_view({'post': 'create'})),
    path("order-detail/<int:id>/", OrderViewSet.as_view({'get': 'retrieve'})),
    ]