from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from catalog.serializers.catalogItem_serializer import CatalogItemSerializer
from catalog.models.product_model import Product

class ProductLimitedViewSet(ModelViewSet):
    """
   ViewSet для отображения ограниченных выпусков продуктов.

   Этот ViewSet предоставляет возможность просмотра продуктов, которые были выпущены в ограниченном количестве.
   Он использует фильтрацию для выбора только ограниченных выпусков и предварительную выборку связанных объектов
   для оптимизации производительности.

   Атрибуты:
   - queryset: Запрос, который выбирает ограниченные выпуски продуктов, упорядоченные по дате.
   - serializer_class: Сериализатор, используемый для преобразования данных продуктов в формат JSON.

   Методы:
   - list: Отображает список ограниченных выпусков продуктов.
   """
    queryset = (
        Product.objects
        .filter(limited_edition=True)
        .prefetch_related("tags", "images", )
        .order_by('date')[:16]
    )
    serializer_class = CatalogItemSerializer

    def list(self, request: Request, *args, **kwargs) -> Response:
        """
        Отображает список ограниченных выпусков продуктов. Возвращает список продуктов, которые были выпущены в
        ограниченном количестве, упорядоченных по дате.

        Параметры:
        - request: Запрос от клиента.

        Возвращает:
        - Response: Ответ, содержащий список продуктов в формате JSON.
        """
        items = self.get_serializer(self.queryset, many=True).data

        return Response(items)