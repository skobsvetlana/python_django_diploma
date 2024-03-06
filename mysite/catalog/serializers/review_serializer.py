from catalog.models.product_model import Review

from rest_framework import serializers


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


    def create(self, validated_data):
        review = Review.objects.create(**validated_data)

        return review

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["author"] = instance.author.first_name

        return data
