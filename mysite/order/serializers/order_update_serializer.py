from rest_framework import serializers

from order.models import Order
from order.serializers.order_create_serializer import OrderItemSerializer

def get_second_last_order(user):
    try:
        second_last_order = Order.objects.filter(customer=user).order_by('-createdAt')[1]
    except IndexError:
        second_last_order = None

    return second_last_order


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

        if instance.customer == None:
            try:
                request = self.context.get('request')
                customer = request.__getattribute__("user")
            except TypeError:
                customer = instance.customer
                print("Type Error: customer is None")
        else:
            customer = instance.customer

        second_last_order = get_second_last_order(customer)
        print("second_last_order", second_last_order)

        if second_last_order:
            representation["fullName"] = second_last_order.fullName
            representation["email"] = second_last_order.email
            representation["phone"] = second_last_order.phone
            representation['city'] = second_last_order.city.name
            representation['address'] = second_last_order.address.address1
        else:
            representation["fullName"] = customer.first_name
            representation["email"] = customer.email
            representation["phone"] = customer.profile.phone

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







