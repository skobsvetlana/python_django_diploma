from catalog.models.product_model import Product
from catalog.serializers.catalogItem_serializer import CatalogItemSerializer

from rest_framework import serializers

from order.models import (
    Order,
    OrderItem,
)


def get_second_last_order(user):
    """
    Получает второй последний заказ пользователя.

    :param user: Пользователь, для которого нужно получить заказ.
    :return: Второй последний заказ пользователя или None, если заказов нет.
    """
    try:
        second_last_order = Order.objects.filter(customer=user).order_by('-createdAt')[1]
        print("This is not the first order")
    except IndexError:
        print("This is the very first order")
        second_last_order = None

    return second_last_order


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для представления продукта в заказе
    """

    class Meta:
        model = OrderItem
        fields = [
            "product",
            "count",
            "price",
        ]

    def to_representation(self, instance):
        """
        Преобразует объект OrderItem в словарь для сериализации.

        :param instance: Объект OrderItem.
        :return: Словарь с данными продукта.
        """
        data = CatalogItemSerializer(instance.product).data
        data['count'] = instance.count
        data['price'] = instance.price

        return data


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для представления заказа и родуктов в нем.
    """
    orderId = serializers.IntegerField(source="pk", read_only=True)
    products = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "orderId",
            "products",
        ]

    def create(self, validated_data):
        """
        Создает новый заказ с продуктами.

        :param validated_data: Данные для создания заказа.
        :return: Созданный заказ.
        """
        order_items = validated_data.pop("products", [])
        order = Order.objects.create(**validated_data)

        for item in order_items:
            product = item.get("product")
            count = item.get("count")

            if product.totalCount < count:
                raise serializers.ValidationError(
                    f"Not enough stock for product {product}. Only {product.totalCount} available.")

            OrderItem.objects.create(order=order, **item)
            product.totalCount -= count
            product.save()

        return order
