from catalog.models.specification_model import Specification

from rest_framework import serializers

class SpecificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = [
            "name",
            "value",
        ]