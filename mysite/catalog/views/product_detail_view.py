from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from catalog.serializers.productFull_serializer import ProductFullSerializer

from catalog.models.product_model import Product

from django.shortcuts import get_object_or_404

class ProductDetailViewSet(ModelViewSet):
    queryset = (
        Product.objects
        .prefetch_related("tags", "specifications", "images", "reviews", ).all()
    )
    serializer_class = ProductFullSerializer

    def retrieve(self, request: Request, id, **kwargs) -> Response:
        item = get_object_or_404(self.queryset, pk=id)
        serializer = self.get_serializer(item)

        return Response(serializer.data)