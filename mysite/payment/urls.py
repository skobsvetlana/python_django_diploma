from django.urls import path, include

from payment.views import PaymentViewset

from rest_framework.routers import DefaultRouter

app_name = "payment"

routers = DefaultRouter()
routers.register("payment", PaymentViewset, basename="payment")

urlpatterns = [
    path("", include(routers.urls)),
    path("payment/<int:id>/", PaymentViewset.as_view({'post': 'create'})),
    ]