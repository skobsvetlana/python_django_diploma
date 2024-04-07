from catalog.models.tag_model import Tag

from rest_framework import serializers

class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Tag.
    Преобразует объекты модели Tag в формат JSON и обратно.
    Поля:
    - id: Уникальный идентификатор тега.
    - name: Название тега.
    """
    class Meta:
        model = Tag
        fields = [
            "id",
            "name",
        ]