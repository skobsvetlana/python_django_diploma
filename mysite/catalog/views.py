from collections import OrderedDict

from rest_framework import pagination, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from catalog.serializers import (ProductFullSerializer,
                                 ProductSerializer,
                                 CategorySerializer,
                                 TagSerializer,
                                 SaleItemSerializer,
                                 CatalogItemSerializer,
                                 )
from catalog.models import Product, Tag, Category, SaleItem

from django.shortcuts import get_object_or_404

class CatalogPagination(pagination.PageNumberPagination):
    page_size = 20
    max_page_size = 50

    def get_paginated_response(self, data):
        return Response(OrderedDict((
            ('items', data),
            ('currentPage', self.page.number),
            ('lastPage', self.page.paginator.count),
        )))


class CatalogViewSet(ModelViewSet):
    serializer_class = CatalogItemSerializer
    queryset = (
        Product.objects
        .prefetch_related("tags", "specifications", "images", "reviews", ).all()
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
        order = self.request.GET["sort"]

        queryset = (self.queryset
                    .filter(price__gte=float(minPrice), price__lte=float(maxPrice))
                    .order_by("price"))

        if available == "true":
            queryset = queryset.filter(totalCount__gt=0)

        if freeDelivery == "true":
            queryset = queryset.filter(free_delivery=True)

        print("freeDelivery=", freeDelivery)
        return queryset

    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()
        # page = request.GET.get('page')
        if queryset.exists():
            page = self.paginate_queryset(queryset)
            if page:
                data = self.get_serializer(page, many=True).data
                print("++++++++++++++++++++++++catalog_item_list")
                print(len(data))
                return self.get_paginated_response(data)
        return Response(status=status.HTTP_404_NOT_FOUND)


class ProductFullViewSet(ModelViewSet):
    queryset = (
        Product.objects
        .prefetch_related("tags", "specifications", "images", "reviews", ).all()
    )
    serializer_class = ProductFullSerializer

    def list(self, request: Request, *args, **kwargs) -> Response:
        items = self.get_serializer(self.queryset, many=True)
        print("++++++++++++++++++++++++productfull_list")
        return Response(items.data)

    def retrieve(self, request, id, **kwargs):
        item = get_object_or_404(self.queryset, pk=id)
        serializer = self.get_serializer(item)
        print("++++++++++++++++++++++++productfull_retrieve")
        return Response(serializer.data)


class LimitedViewSet(ModelViewSet):
    queryset = (
        Product.objects
        .filter(limited_edition=True)
        .prefetch_related("tags", "specifications", "images", "reviews", )
    )
    serializer_class = ProductFullSerializer


class ProductViewSet(ModelViewSet):
    queryset = (
        Product.objects
        .order_by("price")
        .prefetch_related("images", )
    )
    # filter(gender='MALE', price__range=(10, 50))
    serializer_class = ProductSerializer

    def list(self, request: Request, *args, **kwargs) -> Response:
        items = self.get_serializer(self.queryset, many=True).data

        return Response(items)


class SalesViewSet(ModelViewSet):
    queryset = (
        SaleItem.objects.select_related("product").all()
    )
    serializer_class = SaleItemSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
