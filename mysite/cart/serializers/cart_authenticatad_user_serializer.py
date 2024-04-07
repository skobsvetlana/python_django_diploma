from catalog.models.saleItem_model import SaleItem

from catalog.serializers.catalogItem_serializer import CatalogItemSerializer

from rest_framework import serializers


from cart.models import (
    Cart,
    CartItem,
    )


class CartItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для представления продукта в корзине, для зарегистрированных
    пользователей. Включает информацию о продукте и количестве его в корзине.
    """
    #sub_total = serializers.SerializerMethodField(method_name="total")

    class Meta:
        model = CartItem
        fields = [
            "product",
            "count",
            #"sub_total",
        ]

    # def total(self, cart_item: CartItem):
    #     return cart_item.count * cart_item.product.price


    def to_representation(self, instance):
        """
        Переопределение метода to_representation для добавления дополнительной
        информации о продукте, таких как цена со скидкой, если она есть.
        """
        data = CatalogItemSerializer(instance.product).data
        data['count'] = instance.count
        sale_item = SaleItem.objects.filter(product=instance.product).first()

        if sale_item:
            data['price'] = sale_item.salePrice

        return data


class CartSerializer(serializers.ModelSerializer):
    """
    Сериализатор для представления корзины и продуктов в ней, для зарегистрированных
    пользователей. Включает информацию о корзине, такую как общий итог и список
    продуктов.
    """
    #id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    grand_total = serializers.SerializerMethodField(method_name="main_total")

    class Meta:
        model = Cart
        fields = [
            "id",
            "user",
            "createdAt",
            "grand_total",
            "items"
        ]


    def main_total(self, cart: Cart):
        """
        Вычисление общего итога корзины, суммируя цены всех продуктов в корзине.
        """
        items = cart.items.all()
        total = sum([item.count * item.product.price for item in items])
        return total


