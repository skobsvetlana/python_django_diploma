from catalog.models import (Product,
                            Tag,
                            Category,
                            Images,
                            SaleItem,
                            Review,
                            Specification,
                            )

from django.contrib.auth.models import User

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
        ]


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = [
            "src",
            "alt",
        ]


class ReviewsSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False)

    class Meta:
        model = Review
        fields = [
            "author",
            "text",
            "rate",
            "date",
        ]


class SpecificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = [
            "name",
            "value",
        ]


class ProductFullSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True, required=False)
    reviews = ReviewsSerializer(many=True, required=False)
    specifications = SpecificationsSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "title",
            "price",
            "totalCount",
            "date",
            "fullDescription",
            "description",
            "limited_edition",
            "tags",
            "specifications",
            "images",
            "reviews",
        ]


class ProductSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True, required=False)
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "price",
            "category",
            "images",
        ]


class SaleItemSerializer(serializers.ModelSerializer):
    product = ProductFullSerializer(many=False, required=False)

    class Meta:
        model = SaleItem
        fields = [
            "product",
            "salePrice",
            "dateFrom",
            "dateTo",
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            "id",
            "name",
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "title",
            "category_id",
        ]





