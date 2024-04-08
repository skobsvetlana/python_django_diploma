from collections import OrderedDict
from typing import List, Any

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
    """
    Пользовательский класс пагинации для Каталога.
    """
    page_size = 10
    max_page_size = 100
    page_size_query_param = "page_size"
    page_query_param = "currentPage"

    def get_paginated_response(self, data):
        if isinstance(data, list):
            return Response(
                OrderedDict({
                    'items': data,
                    'currentPage': self.page.number,
                    'lastPage': self.page.paginator.num_pages,
                })
            )
        else:
            return Response({"error": "Data is not a list"}, status=400)


def limit_is_valid(limit: Any) -> bool:
    """
    Функция проверяет, является ли переданное значение допустимым размером страницы.
    """
    return ((isinstance(limit, str) and limit.isdigit()) or isinstance(limit, int)) and int(limit) >= 1


class CatalogViewSet(ModelViewSet):
    """
    Пользовательский ViewSet для управления элементами каталога. Он также поддерживает функции фильтрации и
    сортировки, предоставляя API для управления каталогом.

    Атрибуты:
    - serializer_class: Определяет сериализатор, используемый для валидации и преобразования данных.
    - queryset: Определяет начальный queryset для получения элементов каталога, включая предварительную выборку
    связанных объектов и аннотацию с условной ценой.
    - pagination_class: Определяет класс пагинации, используемый для пагинации результатов.

    Методы:
    - get_subcategories: Получает подкатегории для данного ID категории.
    - get_queryset: Динамически генерирует queryset на основе различных фильтров и опций сортировки, предоставленных
    в запросе.
    - list: Обрабатывает GET-запрос для перечисления элементов каталога, применяя фильтры, сортировку и пагинацию,
    как указано в запросе.
    """
    serializer_class = CatalogItemSerializer
    queryset = (
        Product.objects
        .prefetch_related("tags", "images", "category", "reviews", )
        .annotate(
            conditional_price=Coalesce(
                F("saleitem__salePrice"),
                F('price')
            )
        )
    )
    pagination_class = CatalogPagination

    def get_subcategories(self, category_id: int) -> List:
        """
        Получает подкатегории для данного ID категории.

        Параметры:
        - category_id: ID категории, для которой нужно получить подкатегории.

        Возвращает:
        - Список ID подкатегорий.
        """

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
        """
        Генерирует queryset на основе различных фильтров и опций сортировки, предоставленных в запросе.

        Возвращает:
        - Queryset элементов каталога, отфильтрованный и отсортированный в соответствии с параметрами запроса.
        """
        queryset = self.queryset
        minPrice = self.request.GET["filter[minPrice]"]
        maxPrice = self.request.GET["filter[maxPrice]"]
        available = self.request.GET["filter[available]"]
        sortType = self.request.GET["sortType"]
        freeDelivery = self.request.GET["filter[freeDelivery]"]
        sort = self.request.GET["sort"]

        try:
            name = self.request.GET["filter[name]"].lower()
        except MultiValueDictKeyError:
            name = None

        try:
            category_id = self.request.GET["category"]
        except MultiValueDictKeyError:
            category_id = None

        try:
            tags = self.request.GET.getlist("tags[]")
            print("tags", self.request.GET["tags[]"])
        except MultiValueDictKeyError:
            tags = None

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

        if name:
            filter_dict["title__iregex"] = name

        if tags:
            filter_dict["tags__id__in"] = tags
            # queryset = queryset.filter(tags__id__in=tags)
            # queryset = queryset.annotate(matched_tags_count=Count('tags'))
            # filter_dict["matched_tags_count"] = len(tags)

        if sort == "reviews":
            queryset = (Product.objects
            .prefetch_related("tags", "images", "category", "reviews")
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

        if sortType == 'dec':
            sort = f'-{sort}'

        queryset = queryset.filter(**filter_dict).order_by(sort).distinct()

        return queryset

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Обрабатывает GET-запрос для перечисления элементов каталога.

        Параметры:
        - request: HTTP-запрос.

        Возвращает:
        - Пагинированный список элементов каталога или ответ 404 Not Found, если элементы недоступны.
        """

        queryset = self.get_queryset()
        limit = request.query_params.get('limit')

        if limit_is_valid(limit):
            CatalogPagination.page_size = limit

        if queryset.exists():
            page = self.paginate_queryset(queryset=queryset)

            if page is not None:
                data = self.get_serializer(page, many=True).data
                print("++++++++++++++++++++++++catalog_item_list")
                print("len(data)", len(data))
                return self.get_paginated_response(data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        return Response(status=status.HTTP_404_NOT_FOUND)
