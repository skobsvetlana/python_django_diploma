from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from cart.models import Product, Cart, CartItem
from catalog.models import SaleItem

from catalog.serializers import CatalogItemSerializer
from cart.serializers import (
    CartItemSerializer,
    CartSerializer,
    )

def find_index_by_key(data, key, value):
    for index, item in enumerate(data):
        if key in item and item[key] == value:
            return index


class CartViewSet(ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()


class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()

    # def get_queryset(self, *args, **kwargs):
    #     queryset = CartItem.objects.filter(cart__user=self.request.user).prefetch_related()
    #     return queryset

    def update(self, request: Request, *args, **kwargs) -> Response:
        """
        Обновление корзины и продуктов в ней
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        product_id = request.data["id"]
        count = request.data["count"]
        product = Product.objects.get(id=product_id)
        request.session['order_id'] = None

        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)

            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_item.count += int(count)

            cart_item.save()

            cart_items = CartItem.objects.filter(cart=cart)
            serializer = self.get_serializer(cart_items, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # session_key = request.session.session_key
            # session_key = request.get_or_create_session_key()
            cart_items = request.session.get('cart_data', [])
            index = find_index_by_key(cart_items, "id", product.pk)
            sale_item = SaleItem.objects.filter(product=product).first()

            if sale_item:
                product.price = sale_item.salePrice

            if index is not None:
                count += cart_items[index]["count"]
                cart_items.pop(index)

            product.totalCount = count
            item = CatalogItemSerializer(product).data
            cart_items.append(item)
            request.session["cart_data"] = cart_items

        return Response(cart_items, status=status.HTTP_200_OK)


    def list(self, request: Request, *args, **kwargs) -> Response:
        if request.user.is_authenticated:
            serializer = self.get_serializer(self.get_queryset(), many=True)
        else:
            # здесь totalCount заменить на count
            cart_items = request.session.get('cart_data', [])
            product_ids = [item.get('id') for item in cart_items]
            products = Product.objects.filter(pk__in=product_ids)
            serializer = CatalogItemSerializer(products, many=True)

        return Response(serializer.data)


    def destroy(self, request: Request, *args, **kwargs):
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

            if item["count"] > count:
                count = item["count"] - count
                product.totalCount = count
                item = CatalogItemSerializer(product).data
                cart_items.append(item)
                request.session["cart_data"] = cart_items
                request.session.modified = True

            return Response(cart_items, status=status.HTTP_200_OK)

