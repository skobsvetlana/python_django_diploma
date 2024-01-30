from django.urls import path, include

from catalog.views import (ProductViewSet,
                           CategoryViewSet,
                           TagViewSet,
                           LimitedViewSet,
                           SalesViewSet,
                           CatalogViewSet,
                           ProductFullViewSet,
                           )

from rest_framework.routers import DefaultRouter

app_name = "shopapp"

routers = DefaultRouter()
routers.register("catalog", CatalogViewSet, basename="catalog")
routers.register("categories", CategoryViewSet)
routers.register("tags", TagViewSet)
routers.register("products/popular", ProductViewSet)
routers.register("products/limited", LimitedViewSet)
routers.register("sales", SalesViewSet)
routers.register("banners", ProductViewSet)

urlpatterns = [
    path("", include(routers.urls)),
    path("product/<int:id>/", ProductFullViewSet.as_view({'get': 'retrieve'}), name='product_detail'),
    path("catalog", CatalogViewSet.as_view({'get': 'list'}), name='product_list'),
]
