from catalog.models.product_model import Review

from django.contrib.auth.models import User

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
        ]


class ReviewsSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False)

    class Meta:
        model = Review
        fields = '__all__'
