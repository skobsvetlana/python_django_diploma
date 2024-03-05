from catalog.models.images_model import Images

from rest_framework import serializers

class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = [
            "src",
            "alt",
        ]