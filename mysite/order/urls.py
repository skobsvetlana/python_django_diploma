from django.urls import path, include

from order.views import OrderViewSet, OrderDetailViewSet

from rest_framework.routers import DefaultRouter

app_name = "order"

routers = DefaultRouter()
routers.register("order", OrderViewSet, basename="order")
routers.register("orders", OrderViewSet, basename="orders")

urlpatterns = [
    path("", include(routers.urls)),
    path("orders", OrderViewSet.as_view(
        {
            'get': 'list',
            'post': 'create',
        }
    )),
    path("orders/<int:id>/", OrderDetailViewSet.as_view(
        {
            'get': 'retrieve',
            'post': 'update',
        }
    )),
    path("order/<int:id>", OrderDetailViewSet.as_view(
        {
            'get': 'retrieve',
            'post': 'update',
        }
    )),
]