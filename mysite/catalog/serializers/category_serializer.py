from rest_framework_recursive.fields import RecursiveField

from catalog.models.category_model import Category

from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Category, позволяющий сериализовать иерархические категории.
    """
    subcategories = RecursiveField(allow_null=True, many=True)
    # subcategories: Поле для рекурсивного отображения подкатегорий.
    # allow_null: Позволяет подкатегории быть пустыми.
    # many: Указывает, что подкатегории могут быть множественными.

    class Meta:
        model = Category
        fields = [
            "id",
            "title",
            "image",
            "subcategories",
    ]
    # id: Уникальный идентификатор категории.
    # title: Название категории.
    # image: Изображение категории.
    # subcategories: Список подкатегорий, которые могут быть рекурсивно вложены.

