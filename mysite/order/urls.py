from django.urls import path, include

from order.views import OrderViewset

from rest_framework.routers import DefaultRouter

app_name = "order"

routers = DefaultRouter()

from django.urls import path, include

routers.register("order", OrderViewset, basename="order")

urlpatterns = [
    path("", include(routers.urls)),
    ]