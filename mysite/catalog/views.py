from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from catalog.serializers import (ProductFullSerializer,
                                 ProductSerializer,
                                 CategorySerializer,
                                 TagSerializer,
                                 SaleItemSerializer,
                                 )
from catalog.models import Product, Tag, Category, SaleItem

from django.shortcuts import get_object_or_404

class CatalogItemViewSet(ModelViewSet):
    serializer_class = ProductFullSerializer
    queryset = (
        Product.objects
        .prefetch_related("tags", "specifications", "images", "reviews", ).all()
    )

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

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        items = self.get_serializer(queryset, many=True).data
        print("++++++++++++++++++++++++catalog_item_list")
        print(len(items))
        return Response(items)

    def retrieve(self, request, id, **kwargs):
        item = get_object_or_404(self.queryset, pk=id)
        serializer = self.get_serializer(item)
        print("++++++++++++++++++++++++cart_item_retrieve")
        return Response(serializer.data)


class ProductFullViewSet(ModelViewSet):
    queryset = (
        Product.objects
        .prefetch_related("tags", "specifications", "images", "reviews", ).all()
    )
    serializer_class = ProductFullSerializer

    def list(self, request, *args, **kwargs):
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

    def list(self, request, *args, **kwargs):
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







