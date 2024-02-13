from django.contrib.auth.models import User
from catalog.serializers import CatalogItemSerializer

from rest_framework import serializers

from catalog.models import SaleItem
from order.models import (
    Address,
    Order,
    OrderItem
)


class AddressSerializer(serializers.ModelSerializer):
    """
    Сериализатор для представления адреса достакви заказа
    """
    class Meta:
        model = Address
        fields = [
            "address1",
            "address2",
            "zip_code",
            "city",
        ]

class OrderItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для представления продукта в заказе
    """
    product = CatalogItemSerializer(required=True)
    #sub_total = serializers.SerializerMethodField(method_name="total")

    class Meta:
        model = OrderItem
        fields = [
            "product",
            #"sub_total",
        ]

    # def total(self, cart_item: CartItem):
    #     return cart_item.count * cart_item.product.price


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для представления заказа и родуктов в нем.
    """
    items = OrderItemSerializer(many=True,)

    class Meta:
        model = Order
        fields = [
            "id",
            "createdAt",
            "items",
        ]


class OrderDetailsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для полного представления заказа, включая адреса доставки, статуса и прочее,
    а также родуктов в нем.
    """
    #id = serializers.UUIDField(read_only=True)
    address = AddressSerializer(required=True)
    items = OrderItemSerializer(many=True,)
    grand_total = serializers.SerializerMethodField(method_name="main_total")

    class Meta:
        model = Order
        fields = [
            "id",
            "customer",
            "createdAt",
            "paymentType",
            "status",
            "grand_total",
            "address",
            "items",
        ]


    def main_total(self, order: Order):
        items = order.items.all()
        total = sum([item.count * item.product.price for item in items])
        return total
