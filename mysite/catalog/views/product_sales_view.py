from collections import OrderedDict

from rest_framework import pagination, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from catalog.serializers.saleItem_serializer import SaleItemSerializer
from catalog.models.saleItem_model import SaleItem

class SaleItemPagination(pagination.PageNumberPagination):
    page_size = 20
    max_page_size = 50

    def get_paginated_response(self, data):
        return Response(OrderedDict((
            ('items', data),
            ('currentPage', self.page.number),
            ('lastPage', self.page.paginator.num_pages),
        )))

class SalesViewSet(ModelViewSet):
    queryset = (
        SaleItem.objects.select_related("product").all()
    )
    serializer_class = SaleItemSerializer
    pagination_class = SaleItemPagination

    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()
        if queryset.exists():
            page = self.paginate_queryset(queryset)
            if page:
                data = self.get_serializer(page, many=True).data

                return self.get_paginated_response(data)

        return Response(status=status.HTTP_404_NOT_FOUND)

