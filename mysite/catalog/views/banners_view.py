from django.db.models import Min, OuterRef, Subquery, F
from django.db.models.functions import Coalesce

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from catalog.serializers.catalogItem_serializer import CatalogItemSerializer
from catalog.models.product_model import Product


class BannersViewSet(ModelViewSet):
    """
    ViewSet для работы с баннерами продуктов. Предоставляет возможность просмотра и редактирования баннеров,
    включая связанные с ними теги, изображения и категории.

    Атрибуты:
    - queryset: Получает объекты Product с предварительной выборкой связанных тегов, изображений и категории,
      а также аннотирует каждый продукт минимальной ценой в своей категории.
    - serializer_class: Использует CatalogItemSerializer для сериализации данных.

    Методы:
    - get_queryset: Переопределяет метод для получения queryset, включая фильтрацию продуктов с минимальной ценой в их категории.
    - list: Переопределяет метод для получения списка баннеров, используя сериализатор для преобразования данных в формат JSON.
    """
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
        """
        Функция возвращает запрос к базе данных, который выбирает продукты с минимальной ценной в каждой категории.
        Использует подзапросы для вычисления минимальной цены в каждой категории и фильтрации продуктов по этой цене.
        """
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
        """
        Функция обрабатывает GET запрос для получения списка продуктов с минимальной ценной в каждой категории.
        Возвращает сериализованные данные продуктов в формате JSON.
        """
        items = self.get_serializer(self.get_queryset(), many=True).data

        return Response(items)
