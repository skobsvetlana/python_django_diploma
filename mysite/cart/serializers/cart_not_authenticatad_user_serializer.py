from catalog.models.product_model import Product
from catalog.models.saleItem_model import SaleItem

from rest_framework import serializers

from catalog.serializers.image_serializer import ImagesSerializer
from catalog.serializers.tag_serializer import TagSerializer

class CartItemUserNotAuthenticatedSerializer(serializers.ModelSerializer):
    """
    Сериализатор для представления продукта в корзине, для незарегистрированных
    пользователей. Включает информацию о продукте, такую как изображения, теги,
    количество на складе, информацию о бесплатной доставке, отзывы и рейтинг.
    """
    images = ImagesSerializer(many=True, required=True)
    tags = TagSerializer(many=True, required=False)
    count = serializers.SerializerMethodField(method_name="get_count")
    freeDelivery = serializers.SerializerMethodField(method_name="get_freeDelivery")
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
        """
        Возвращает общее количество продукта на складе.
        """
        return product.totalCount

    def get_freeDelivery(self, product: Product):
        """
        Возвращает информацию о бесплатной доставке для продукта.
        """
        return product.free_delivery

    def get_reviews(self, product: Product):
        """
        Возвращает количество отзывов для продукта.
        """
        return product.reviews_count

    def to_representation(self, instance):
        """
        Переопределение метода to_representation для корректировки данных
        продукта в зависимости от контекста запроса.
        """
        data = super().to_representation(instance)

        if self.context.get('view').action == 'list':
            cart_data = self.context.get('cart_items', [])

            for item in cart_data:
                if item.get('id') == instance.pk:
                    data['count'] = item.get('count', data['count'])
                    break
        else:
            count = self.context.get('count', instance.totalCount)
            data['count'] = count

        sale_item = SaleItem.objects.filter(product=instance.pk).first()

        if sale_item:
            data['price'] = float(sale_item.salePrice)

        return data

#
# class CartUserNotAuthenticatedSerializer(serializers.Serializer):
#     """
#     Сериализатор для представления корзины и продуктов в ней, для незарегистрированных
#     пользователей
#     """
#     items = CartItemUserNotAuthenticatedSerializer(many=True, read_only=True)
#
#     class Meta:
#         fields = [
#             "items"
#         ]


