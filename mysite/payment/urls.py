from django.urls import path, include

from payment.views import PaymentViewset

from rest_framework.routers import DefaultRouter

app_name = "payment"

routers = DefaultRouter()

from django.urls import path, include

routers.register("payment", PaymentViewset, basename="payment")

urlpatterns = [
    path("", include(routers.urls)),
    ]