from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from catalog.serializers.tag_serializer import TagSerializer
from catalog.models.tag_model import Tag

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def list(self, request: Request, *args, **kwargs) -> Response:
        items = self.get_serializer(self.queryset, many=True).data

        return Response(items)