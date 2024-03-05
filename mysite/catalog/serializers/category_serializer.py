from rest_framework_recursive.fields import RecursiveField

from catalog.models.category_model import Category

from rest_framework import serializers


class SubCategorySerializer(serializers.ModelSerializer):
    pass


class CategorySerializer(serializers.ModelSerializer):
    subcategories = RecursiveField(allow_null=True, many=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "title",
            "image",
            "subcategories",
        ]



# class CategorySerializer(serializers.ModelSerializer):
#     subcategories = RecursiveField(allow_null=True, many=True)
#
#     class Meta:
#         model = Category
#         fields = [
#             "id",
#             "title",
#             "image",
#             "subcategories",
#         ]