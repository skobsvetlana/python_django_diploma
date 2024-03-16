from django.db.models import Sum, F, Count
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.request import Request

from catalog.serializers.catalogItem_serializer import CatalogItemSerializer
from catalog.models.product_model import Product


class ProductPopularViewSet(ModelViewSet):
    queryset = (
        Product.objects
        .prefetch_related("tags", "images", )
        # .annotate(
        #     total_revenue=Sum(F('order_item__price') * F('order_item__count'))
        # )
        .annotate(
            total_revenue=Sum('order_item__price', multiplier='order_item__count'),
            sold_count=Count('order_item')
        )
        .order_by('-total_revenue', '-sold_count')[:8]
    )
    serializer_class = CatalogItemSerializer

    def list(self, request: Request, *args, **kwargs) -> Response:
        items = self.get_serializer(self.queryset, many=True).data
        print(len(self.queryset))
        return Response(items)
