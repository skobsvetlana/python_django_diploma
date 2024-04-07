from catalog.models.images_model import Images

from rest_framework import serializers

class ImagesSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Images.
    Преобразует объекты модели Images в JSON и обратно.
    """
    class Meta:
        model = Images
        fields = [
            "src",
            "alt",
        ]