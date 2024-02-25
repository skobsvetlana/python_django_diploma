from catalog.serializers import CatalogItemSerializer

from rest_framework import serializers

from order.models import (
    Address,
    Order,
    OrderItem,
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
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для представления продукта в заказе
    """
    # product = CatalogItemSerializer()

    class Meta:
        model = OrderItem
        fields = [
            "product",
            "count",
            "price",
        ]


    def to_representation(self, instance):
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
        order_items = validated_data.pop("products", [])
        order = Order.objects.create(**validated_data)

        for item in order_items:
            OrderItem.objects.create(order=order, **item)

        return order


class OrderDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для полного представления заказа, включая адреса доставки, статуса и прочее,
    а также родуктов в нем.
    """
    products = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "createdAt",
            "fullName",
            "email",
            "phone",
            "deliveryType",
            "paymentType",
            "totalCost",
            "status",
            "products",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if instance.address is None:
            address = Address.objects.create(address1="", address2="", city="", zip_code="",)
            instance.address = address

        representation['city'] = instance.address.city
        representation['address'] = instance.address.address1
        instance.save()

        return representation

    def update(self, instance, validated_data):
        """
        Изменяет и возвращает данные получателе заказа, адрес.
        """
        instance.fullName = validated_data.get('fullName', instance.fullName)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.deliveryType = validated_data.get('deliveryType', instance.deliveryType)
        instance.paymentType = validated_data.get('paymentType', instance.paymentType)
        instance.address.address1 = validated_data.get('address', instance.address.address1)
        instance.address.city = validated_data.get('city', instance.address.city)
        instance.address.save()
        instance.save()

        return instance







