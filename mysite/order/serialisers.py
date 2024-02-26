from catalog.serializers import CatalogItemSerializer

from rest_framework import serializers

from order.models import (
    Address,
    Order,
    OrderItem,
    City,
)

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
    address = serializers.CharField()
    city = serializers.CharField()

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
            "address",
            "city",
            "products",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')

        if request and hasattr(request, 'user'):
            customer = request.user

        try:
            second_last_order = Order.objects.filter(customer=instance.customer).order_by('-createdAt')[1]
            print("This is not the first order")
        except IndexError:
            print("This is the very first order")
            second_last_order = None

        if second_last_order:
            representation["fullName"] = second_last_order.fullName
            representation["email"] = second_last_order.email
            representation["phone"] = second_last_order.phone
            representation['city'] = second_last_order.city.name
            representation['address'] = second_last_order.address.address1
        else:
            representation["fullName"] = instance.customer.first_name
            representation["email"] = instance.customer.email
            representation["phone"] = instance.customer.profile.phone
            representation['city'] = instance.city.name
            representation['address'] = instance.address.address1


        return representation


    def update(self, instance, validated_data):
        """
        Изменяет и возвращает данные получателе заказа.
        """
        instance.fullName = validated_data.get('fullName', instance.fullName)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.deliveryType = validated_data.get('deliveryType', instance.deliveryType)
        instance.paymentType = validated_data.get('paymentType', instance.paymentType)
        instance.address = validated_data.get('address', instance.address)
        instance.city = validated_data.get('city', instance.city)
        instance.save()

        return instance







