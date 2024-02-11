from django.contrib.auth.models import User
from catalog.serializers import CatalogItemSerializer

from rest_framework import serializers

from cart.models import (
    Cart,
    CartItem,
    )

class CartItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для представления продукта в корзине
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
        data = CatalogItemSerializer(instance.product).data
        data['count'] = instance.count
        return data


class CartSerializer(serializers.ModelSerializer):
    """
    Сериализатор для представления корзины и продуктов в ней
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
        items = cart.items.all()
        total = sum([item.count * item.product.price for item in items])
        return total

