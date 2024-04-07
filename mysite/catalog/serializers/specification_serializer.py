from catalog.models.specification_model import Specification

from rest_framework import serializers

class SpecificationsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Specification.
    Преобразует объекты модели Specification в формат JSON и обратно.
    """
    class Meta:
        model = Specification
        fields = [
            "name",
            "value",
        ]