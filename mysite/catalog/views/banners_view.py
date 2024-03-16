from django.db.models import Min, OuterRef, Subquery, F
from django.db.models.functions import Coalesce

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from catalog.serializers.catalogItem_serializer import CatalogItemSerializer
from catalog.models.product_model import Product


class BannersViewSet(ModelViewSet):
    queryset = (
        Product.objects
        .prefetch_related("tags", "images", "category")
        .annotate(
            conditional_price=Coalesce(
                F("saleitem__salePrice"),
                F('price')
            )
        )
    )
    serializer_class = CatalogItemSerializer

    def get_queryset(self):
        min_price_subquery = (self.queryset
                              .filter(category=OuterRef('category'))
                              .values('category')
                              .annotate(min_price=Min('conditional_price'))
                              .values('min_price')
                              )
        products_with_min_price = (self.queryset
                                   .annotate(min_price_in_category=Subquery(min_price_subquery))
                                   .filter(conditional_price=F('min_price_in_category'))
                                   )

        return products_with_min_price

    def list(self, request: Request, *args, **kwargs) -> Response:
        items = self.get_serializer(self.get_queryset(), many=True).data

        return Response(items)
