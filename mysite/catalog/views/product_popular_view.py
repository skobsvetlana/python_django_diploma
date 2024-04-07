from django.db.models import Sum, F, Count
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.request import Request

from catalog.serializers.catalogItem_serializer import CatalogItemSerializer
from catalog.models.product_model import Product


class ProductPopularViewSet(ModelViewSet):
    """
     ViewSet для отображения популярных товаров.
     Этот класс использует ModelViewSet для предоставления стандартных
     действий CRUD (создание, чтение, обновление, удаление) для модели Product.
     Он также включает в себя сортировку товаров по общему доходу и количеству продаж, чтобы
     показать наиболее популярные товары.

     Атрибуты:
     - queryset: Запрос к базе данных, который выбирает товары с учетом
       их популярности, используя аннотации для расчета общего дохода и
       количества продаж.
     - serializer_class: Сериализатор, который определяет, как модель Product
       будет преобразована в JSON для отправки в ответе API.

     Методы:
     - list: Переопределенный метод для отображения списка товаров,
       включая пагинацию и сортировку.
     """
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
        """
        Отображает список популярных товаров с сортировкой.
        Этот метод переопределяет стандартный метод list для ModelViewSet,
        чтобы включить в себя пагинацию и сортировку товаров по общему доходу
        и количеству продаж. Он также использует сериализатор для преобразования
        данных модели в формат JSON.

        Параметры:
        - request: Объект запроса, содержащий информацию о запросе клиента.

        Возвращает:
        - Response: Ответ API, содержащий список популярных товаров в формате JSON.
        """
        items = self.get_serializer(self.queryset, many=True).data

        return Response(items)
