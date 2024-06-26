from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from catalog.serializers.tag_serializer import TagSerializer
from catalog.models.tag_model import Tag

class TagViewSet(ModelViewSet):
    """
    ViewSet для работы с тегами.
    Предоставляет операции создания, чтения, обновления и удаления тегов.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

