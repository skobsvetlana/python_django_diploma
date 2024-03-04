from django.contrib.auth.models import User
from catalog.serializers import CatalogItemSerializer

from rest_framework import serializers

from catalog.models import SaleItem, Product
from cart.models import (
    Cart,
    CartItem,
    )

class CartItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для представления продукта в корзине, для зарегистрированных
    пользователей
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
    Сериализатор для представления корзины и продуктов в ней, для зарегистрированных
    пользователей
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
    """
    Сериализатор для представления продукта в корзине, для незарегистрированных
    пользователей
    """
    product = serializers.IntegerField()
    count = serializers.IntegerField()

    def validate(self, attrs, instance=None):
        try:
            data = CatalogItemSerializer(instance.product).data
        except Product.DoesNotExist:
            raise serializers.ValidationError("Продукт с данным ID не найден.")

        return attrs


    def to_representation(self, instance=None):
        data = CatalogItemSerializer(product).data
        data['count'] = instance.count
        sale_item = SaleItem.objects.filter(product=instance.product).first()

        if sale_item:
            data['price'] = sale_item.salePrice

        return data


class CartSerializer(serializers.Serializer):
    """
    Сериализатор для представления корзины и продуктов в ней, для незарегистрированных
    пользователей
    """
    items = CartItemForSessionSerializer(many=True, read_only=True)

    class Meta:
        fields = [
            "items"
        ]


"""
 request = self.context.get('request')

        if request and not request.user.is_authenticated:
            print("+++++++++++++++++++++++++++++++++")
            cart_data = request.session.get('cart_data', [])
            #item_in_cart = next((item for item in cart_data if item.get('id') == instance.pk), None)
            print("---------------------------------")
            # print("item_in_cart", item_in_cart)
            # data = [{key: item.get(key, None) for key in keys} for item in data]
            # print("item_in_cart", item_in_cart)
            # if item_in_cart:
            #     data['count'] = item_in_cart['count']

"""