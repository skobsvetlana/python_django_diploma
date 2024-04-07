from collections import OrderedDict

from rest_framework import pagination, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from catalog.serializers.saleItem_serializer import SaleItemSerializer
from catalog.models.saleItem_model import SaleItem

class SaleItemPagination(pagination.PageNumberPagination):
    """
    Класс для пагинации списка товаров со скидками.
    """
    page_size = 20
    max_page_size = 50
    page_size_query_param = "page_size"
    page_query_param = "currentPage"

    def get_paginated_response(self, data):
        """
        Возвращает ответ с пагинированными данными.

        :param data: Сериализованные данные текущей страницы.
        :return: Response с пагинированными данными.
        """
        return Response(OrderedDict((
            ('items', data),
            ('currentPage', self.page.number),
            ('lastPage', self.page.paginator.num_pages),
        )))

class SalesViewSet(ModelViewSet):
    """
    ViewSet для работы со списком товаров со скидками.
    """
    queryset = (
        SaleItem.objects.select_related("product").all()
    )
    serializer_class = SaleItemSerializer
    pagination_class = SaleItemPagination

    def list(self, request: Request, *args, **kwargs) -> Response:
        """
        Обрабатывает GET-запрос для получения списка товаров со скидками.

        :param request: Запрос от клиента.
        :return: Response с пагинированными данными продаж.
        """
        queryset = self.get_queryset()
        if queryset.exists():
            page = self.paginate_queryset(queryset)
            if page:
                data = self.get_serializer(page, many=True).data

                return self.get_paginated_response(data)

        return Response(status=status.HTTP_404_NOT_FOUND)

