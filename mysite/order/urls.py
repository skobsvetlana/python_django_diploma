from django.urls import path, include

from order.views.order_create_view import OrderViewSet
from order.views.order_update_view import OrderDetailViewSet

from rest_framework.routers import DefaultRouter

app_name = "order"

routers = DefaultRouter()
# routers.register("order", OrderDetailViewSet, basename="order")
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
    path("order/<int:id>/", OrderDetailViewSet.as_view(
                {
                    'get': 'retrieve',
                    'post': 'update',
                }
            )),
]