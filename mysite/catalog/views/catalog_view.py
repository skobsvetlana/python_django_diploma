from collections import OrderedDict
from typing import List

from django.db.models import F, Avg, Count
from django.db.models.functions import Coalesce
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
        .prefetch_related("tags", "images", "category")
        .annotate(
            conditional_price=Coalesce(
                F("saleitem__salePrice"),
                F('price')
            )
        )
    )
    pagination_class = CatalogPagination

    def get_subcategories(self, category_id: int) -> List:
        category = Category.objects.get(pk=category_id)

        if category.parent is None:
            subcategories = (Category.objects
                             .filter(parent=category_id)
                             .values_list('pk', flat=True)
                             )
        else:
            subcategories = category_id,

        return subcategories

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

        filter_dict = {
            "price__gte": float(minPrice),
            "price__lte": float(maxPrice)
        }

        if available == "true":
            filter_dict["totalCount__gt"] = 0
        if freeDelivery == "true":
            filter_dict["free_delivery"] = True
        if category_id is not None:
            subcategories = self.get_subcategories(category_id)
            filter_dict["category__id__in"] = subcategories
        if sort == "reviews":
            queryset = (Product.objects
            .prefetch_related("tags", "images", "category")
            .annotate(
                review_count=Count("reviews")
            ))
            sort = "review_count"
        elif sort == "rating":
            queryset = (Product.objects
            .prefetch_related("tags", "images", "category")
            .annotate(
                avg_rating=Avg("reviews__rate")
            ))
            sort = "avg_rating"
        elif sort == "price":
            sort = "conditional_price"
            queryset = self.queryset
        else:
            queryset = self.queryset
        if sortType == 'dec':
            sort = f'-{sort}'

        queryset = queryset.filter(**filter_dict).order_by(sort)

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
