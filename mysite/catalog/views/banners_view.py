from django.db.models import Min, OuterRef, Subquery, F, Case, When, DecimalField, Value
from django.db.models.functions import Coalesce
from rest_framework.fields import FloatField
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from catalog.models.category_model import Category
from catalog.serializers.catalogItem_serializer import CatalogItemSerializer
from catalog.models.product_model import Product


class BannersViewSet(ModelViewSet):
    queryset = (
        Product.objects
        .prefetch_related("tags", "images", )
    )
    serializer_class = CatalogItemSerializer

    def get_queryset(self):
        min_price_subquery = Product.objects.filter(category=OuterRef('category')).values('category').annotate(
            min_price=Min('price')).values('min_price')
        products_with_min_price = (Product.objects
        .prefetch_related('tags', 'images')
        .annotate(min_price_in_category=Subquery(min_price_subquery)).filter(
            price=F('min_price_in_category')))

        # products_with_min_price = Product.objects.annotate(
        #     min_price=Coalesce(
        #         F('saleitem__salePrice'),  # Use saleItem.salePrice if available
        #         F('price')  # Otherwise, use product.price
        #     )
        # )
        # print(products_with_min_price)
        # subcategories_with_min_price = Category.objects.filter(
        #     subcategories__isnull=False
        # ).annotate(
        #     min_price_in_subcategory=Min('subcategories__min_price')
        # )
        # products_with_min_price_in_subcategory = products_with_min_price.filter(
        #     min_price=F('category__min_price_in_subcategory')
        # )

        return products_with_min_price


    def list(self, request: Request, *args, **kwargs) -> Response:
        items = self.get_serializer(self.get_queryset(), many=True).data

        return Response(items)
