from collections import OrderedDict

from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import pagination, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from catalog.models.category_model import Category
from catalog.serializers.catalogItem_serializer import CatalogItemSerializer
from catalog.models.product_model import Product

class CatalogPagination(pagination.PageNumberPagination):
    page_size = 20
    max_page_size = 50

    def get_paginated_response(self, data):
        return Response(OrderedDict((
            ('items', data),
            ('currentPage', self.page.number),
            ('lastPage', self.page.paginator.num_pages),
        )))


class CatalogViewSet(ModelViewSet):
    serializer_class = CatalogItemSerializer
    queryset = (
        Product.objects
        .prefetch_related("tags", "images",).all()
    )
    pagination_class = CatalogPagination

    def get_queryset(self, *args, **kwargs):
        minPrice = self.request.GET["filter[minPrice]"]
        maxPrice = self.request.GET["filter[maxPrice]"]
        available = self.request.GET["filter[available]"]
        sortType = self.request.GET["sortType"]
        freeDelivery = self.request.GET["filter[freeDelivery]"]
        sort = self.request.GET["sort"]
        limit = self.request.GET["limit"]

        try:
            category_id = self.request.GET["category"]
        except MultiValueDictKeyError:
            category_id = None

        if sortType == 'dec':
            sort = f'-{sort}'

        queryset = (self.queryset
                    .filter(price__gte=float(minPrice), price__lte=float(maxPrice))
                    .order_by(sort))

        if category_id is not None:
            subcategories = (Category.objects
                             .filter(parent=category_id)
                             .values_list('pk', flat=True)
                             )
            if len(subcategories) == 0:
                subcategories = category_id,
            queryset = queryset.filter(category__id__in=subcategories)

        if available == "true":
            queryset = queryset.filter(totalCount__gt=0)

        if freeDelivery == "true":
            queryset = queryset.filter(free_delivery=True)

        print("freeDelivery=", freeDelivery)
        return queryset


    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()

        if queryset.exists():
            page = self.paginate_queryset(queryset)

            if page:
                data = self.get_serializer(page, many=True).data
                print("++++++++++++++++++++++++catalog_item_list")
                print("len(data)", len(data))
                return self.get_paginated_response(data)

        return Response(status=status.HTTP_404_NOT_FOUND)