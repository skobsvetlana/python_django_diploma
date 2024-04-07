from rest_framework import serializers

from catalog.models.product_model import Product
from catalog.models.saleItem_model import SaleItem

from catalog.serializers.image_serializer import ImagesSerializer
from catalog.serializers.tag_serializer import TagSerializer


class CatalogItemSerializer(serializers.ModelSerializer):
    """Сериализатор для элементов каталога продуктов."""
    images = ImagesSerializer(many=True, required=True)
    tags = TagSerializer(many=True, required=False)
    count = serializers.SerializerMethodField(method_name="get_count")
    price = serializers.SerializerMethodField(method_name="get_price")
    freeDelivery = serializers.SerializerMethodField(method_name="get_freeDelivery")
    date = serializers.SerializerMethodField(method_name="date_to_string")
    reviews = serializers.SerializerMethodField(method_name="get_reviews")

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "rating",
        ]

    def get_count(self, product: Product):
        """Возвращает общее количество продукта."""
        return product.totalCount

    def get_price(self, product: Product):
        """Возвращает цену продукта."""
        return float(product.price)

    def date_to_string(self, product: Product):
        """Преобразует дату продукта в строку."""
        return product.date.strftime("%a %b %d %Y %H:%M:%S GMT%z %Z")

    def get_freeDelivery(self, product: Product):
        """Возвращает информацию о бесплатной доставке продукта."""
        return product.free_delivery

    def get_reviews(self, product: Product):
        """Возвращает количество отзывов на продукт."""
        return product.reviews_count

    def to_representation(self, instance):
        """Переопределение метода для изменения представления данных."""
        data = super().to_representation(instance)
        sale_item = SaleItem.objects.filter(product=instance.pk).first()

        if sale_item:
            data['price'] = float(sale_item.salePrice)

        return data

