from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from catalog.serializers.catalogItem_serializer import CatalogItemSerializer
from catalog.models.product_model import Product

class BannersViewSet(ModelViewSet):
    queryset = (
        Product.objects
        .filter(limited_edition=True)
        .prefetch_related("tags", "images",)
    )
    serializer_class = CatalogItemSerializer

    def list(self, request: Request, *args, **kwargs) -> Response:
        items = self.get_serializer(self.queryset, many=True).data

        return Response(items)
