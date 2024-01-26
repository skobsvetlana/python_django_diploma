from django.urls import path, include

from cart.views import (CartItemViewSet,
                        # CartViewSet,
                        )

from rest_framework.routers import DefaultRouter

app_name = "cart"

routers = DefaultRouter()
routers.register("basket", CartItemViewSet, basename="basket")

urlpatterns = [
    path("", include(routers.urls)),
    path("basket", CartItemViewSet.as_view({'get': 'list',
                                            'post': 'update',
                                            })),
]
