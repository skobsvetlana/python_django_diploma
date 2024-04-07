from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from cart.models import Cart, CartItem
from catalog.models.product_model import Product

from cart.serializers.cart_authenticatad_user_serializer import (
    CartItemSerializer,
    CartSerializer,
)
from cart.serializers.cart_not_authenticatad_user_serializer import (
    CartItemUserNotAuthenticatedSerializer,
)


def find_index_by_key(data, key, value):
    """
    Находит индекс элемента в списке словарей по ключу и значению.

    :param data: Список словарей.
    :param key: Ключ для поиска.
    :param value: Значение для поиска.
    :return: Индекс найденного элемента или None, если элемент не найден.
    """
    for index, item in enumerate(data):
        if key in item and item[key] == value:
            return index


def filter_data(data):
    """
    Фильтрует данные, оставляя только ключи "id" и "count".

    :param data: Список словарей для фильтрации.
    :return: Фильтрованный список словарей.
    """
    keys = ["id", "count"]
    data = [{key: item.get(key, None) for key in keys} for item in data]

    for item in data:
        item["product"] = item.pop("id")

    return data


class CartViewSet(ModelViewSet):
    """
    ViewSet для работы с корзиной.
    """
    serializer_class = CartSerializer
    queryset = Cart.objects.all()


class CartItemViewSet(ModelViewSet):
    """
    ViewSet для работы с элементами корзины.
    """
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()

    def update(self, request: Request, *args, **kwargs) -> Response:
        """
        Обновление корзины и продуктов в ней
        """
        product_id = request.data["id"]
        count = request.data["count"]
        product = Product.objects.get(id=product_id)
        request.session['order_id'] = None

        if product.totalCount <= 0:
            raise ValueError(
                f"{product} is out of stock.")

        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

            if int(product.totalCount) > cart_item.count + int(count):
                cart_item.count += int(count)
            else:
                cart_item.count = product.totalCount

            cart_item.save()
            cart_items = CartItem.objects.filter(cart=cart)
            serializer = self.get_serializer(cart_items, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # session_key = request.session.session_key
            # session_key = request.get_or_create_session_key()
            cart_items = request.session.get('cart_data', [])
            index = find_index_by_key(cart_items, "id", product.pk)
            context = self.get_serializer_context()
            context.update({"count": count})

            if index is not None:
                count += cart_items[index]["count"]
                context.update({"count": count})
                cart_items.pop(index)
            item = CartItemUserNotAuthenticatedSerializer(product, context=context).data
            cart_items.append(item)
            request.session["cart_data"] = cart_items

        return Response(cart_items, status=status.HTTP_200_OK)


    def list(self, request: Request, *args, **kwargs) -> Response:
        """
        Получение списка элементов корзины.
        """
        if request.user.is_authenticated:
            serializer = self.get_serializer(self.get_queryset(), many=True)
        else:
            cart_items = request.session.get('cart_data', [])
            context = self.get_serializer_context()
            context.update({"cart_items": cart_items})
            product_ids = [item.get('id') for item in cart_items]
            products = Product.objects.filter(pk__in=product_ids)
            serializer = CartItemUserNotAuthenticatedSerializer(products,
                                                                many=True,
                                                                context=context
                                                                )

        return Response(serializer.data)


    def destroy(self, request: Request, *args, **kwargs):
        """
        Уменьшает количество товара в корзине. Удаляет в случае, если его количесво уменьшается до нуля.
        """
        product_id = request.data["id"]
        count = request.data["count"]
        product = Product.objects.get(id=product_id)

        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

            if cart_item.count > count:
                cart_item.count -= count
                cart_item.save()
            else:
                cart_item.delete()

            cart_items = CartItem.objects.filter(cart=cart)
            serializer = self.get_serializer(cart_items, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            cart_items = request.session.get('cart_data', [])
            index = find_index_by_key(cart_items, "id", product.pk)
            item = cart_items.pop(index)

            if item["count"] >= count:
                count = item["count"] - count

                if count > 0:
                    context = self.get_serializer_context()
                    context.update({"count": count})
                    item = CartItemUserNotAuthenticatedSerializer(product, context=context).data
                    cart_items.append(item)
            request.session["cart_data"] = cart_items
            request.session.modified = True

            return Response(cart_items, status=status.HTTP_200_OK)

