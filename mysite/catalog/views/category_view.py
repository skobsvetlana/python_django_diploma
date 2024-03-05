from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from catalog.serializers.category_serializer import CategorySerializer
from catalog.models.category_model import Category

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # def list(self, request: Request, *args, **kwargs) -> Response:
    #     items = self.get_serializer(self.queryset, many=True).data
    #
    #     return Response(items)