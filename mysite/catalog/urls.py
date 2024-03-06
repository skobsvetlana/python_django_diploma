from django.urls import path, include

from catalog.views.category_view import CategoryViewSet
from catalog.views.catalog_view import CatalogViewSet
from catalog.views.product_detail_view import ProductDetailViewSet
from catalog.views.product_limited_view import ProductLimitedViewSet
from catalog.views.product_sales_view import SalesViewSet
from catalog.views.product_popular_view import ProductPopularViewSet
from catalog.views.banners_view import BannersViewSet
from catalog.views.tag_view import TagViewSet
from catalog.views.review_view import ReviewViewSet

from rest_framework.routers import DefaultRouter

app_name = "catalog"

routers = DefaultRouter()
routers.register("catalog", CatalogViewSet, basename="catalog")
routers.register("categories", CategoryViewSet)
routers.register("tags", TagViewSet)
routers.register("products/popular", ProductPopularViewSet)
routers.register("products/limited", ProductLimitedViewSet)
routers.register("sales", SalesViewSet)
routers.register("banners", BannersViewSet)

urlpatterns = [
    path("", include(routers.urls)),
    path("product/<int:id>", ProductDetailViewSet.as_view({'get': 'retrieve'}), name='product_detail'),
    path("product/<int:id>/", ProductDetailViewSet.as_view({'get': 'retrieve'}), name='_product_detail'),
    path("product/<int:id>/reviews", ReviewViewSet.as_view({'post': 'create'}), name='product_review'),
]
