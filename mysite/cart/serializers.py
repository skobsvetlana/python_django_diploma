from django.contrib.auth.models import User
from catalog.serializers import ProductSerializer

from rest_framework import serializers

from cart.models import (Cart,
                     CartItem,
                     )

class CartItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для представления корзины и продуктов в ней
    """

    #product = ProductFullSerializer(many=False)
    #id = serializers.SerializerMethodField(method_name="product_id")
    #sub_total = serializers.SerializerMethodField(method_name="total")

    class Meta:
        model = CartItem
        fields = [
            #"id",
            "product",
            "count",
            #"sub_total",
        ]

    # def total(self, cart_item: CartItem):
    #     return cart_item.count * cart_item.product.price
    #
    # def product_id(self, cart_item: CartItem):
    #     return cart_item.product.pk

    def to_representation(self, instance):
        data = ProductSerializer(instance.product).data
        data['count'] = instance.count
        return data


class CartSerializer(serializers.ModelSerializer):
    #id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    grand_total = serializers.SerializerMethodField(method_name="main_total")

    class Meta:
        model = Cart
        fields = ["id", "user","createdAt", "grand_total", "items"]
        #fields = ["pk", "createdAt", "items"]

    def main_total(self, cart: Cart):
        items = cart.items.all()
        total = sum([item.count * item.product.price for item in items])
        return total

