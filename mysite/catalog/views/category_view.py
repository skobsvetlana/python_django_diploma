from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from catalog.serializers.category_serializer import CategorySerializer
from catalog.models.category_model import Category

class CategoryViewSet(ModelViewSet):
    """
    ViewSet для просмотра и редактирования категорий.
    Фильтрует queryset, чтобы включить только категории верхнего уровня (те, у которых нет родителя).
    """
    queryset = Category.objects.filter(parent__isnull=True)
    serializer_class = CategorySerializer

