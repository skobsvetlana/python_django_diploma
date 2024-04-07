from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from catalog.serializers.productFull_serializer import ProductFullSerializer

from catalog.models.product_model import Product

from django.shortcuts import get_object_or_404


class ProductDetailViewSet(ModelViewSet):
    """
    ViewSet для просмотра и редактирования детальной информации о конкретном продукте.

    Этот ViewSet предоставляет HTTP метод `GET` для получения экземпляра конкретного продукта,
    включая связанные теги, спецификации, изображения и отзывы.

    Атрибуты:
        queryset (QuerySet): QuerySet, который включает все экземпляры Product, предварительно загружая
        связанные объекты для оптимизации.
        serializer_class (ProductFullSerializer): Класс сериализатора, используемый для преобразования экземпляров
        Product в JSON.

    Методы:
        retrieve(request, id, **kwargs): Получает экземпляр одного продукта на основе его первичного ключа (id).
    """
    queryset = (
        Product.objects
        .prefetch_related("tags", "specifications", "images", "reviews", )
        .all()
    )
    serializer_class = ProductFullSerializer

    def retrieve(self, request: Request, id, **kwargs) -> Response:
        """
        Получает экземпляр класса на основе его первичного ключа.

        Параметры:
        - request: Полученный сервером HTTP запрос.
        - id: Первичный ключ объекта, который нужно получить.
        - **kwargs: Дополнительные ключевые аргументы.

        Возвращает:
        - Объект `Response`, содержащий сериализованные данные полученного объекта.
        """
        item: Product = get_object_or_404(self.queryset, pk=id)
        serializer = self.get_serializer(item)

        return Response(serializer.data)
