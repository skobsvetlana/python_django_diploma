from django.contrib.auth.models import User
from catalog.serializers import CatalogItemSerializer

from rest_framework import serializers

from catalog.models import SaleItem
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
        sale_item = SaleItem.objects.filter(product=instance.product).first()

        if sale_item:
            data['price'] = sale_item.salePrice

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


class CartItemForSessionSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate(self, attrs):
        # Проверьте, существует ли продукт с данным ID
        try:
            data = CatalogItemSerializer(instance.product).data
        except Product.DoesNotExist:
            raise serializers.ValidationError("Продукт с данным ID не найден.")
        return attrs
