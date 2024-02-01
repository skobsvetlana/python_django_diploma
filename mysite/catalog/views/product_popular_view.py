from rest_framework.viewsets import ModelViewSet

from catalog.serializers import CatalogItemSerializer
from catalog.models import Product
from rest_framework.response import Response
from rest_framework.request import Request

class ProductPopularViewSet(ModelViewSet):
    queryset = (
        Product.objects
        .filter(free_delivery=True)
        .prefetch_related("tags", "images",)
    )
    serializer_class = CatalogItemSerializer

    def list(self, request: Request, *args, **kwargs) -> Response:
        items = self.get_serializer(self.queryset, many=True).data

        return Response(items)