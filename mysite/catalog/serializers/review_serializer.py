from catalog.models.product_model import Review

from rest_framework import serializers

class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


    def create(self, validated_data):
        review = Review.objects.create(**validated_data)

        return review

    def validate(self, data):
        product = data.get('product')
        user = self.context['request'].user

        if Review.objects.filter(product=product, user=user).exists():
            raise serializers.ValidationError("This user has already added a review for this product.")

        return data
