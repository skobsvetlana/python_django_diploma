from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from cart.models import Product, Cart, CartItem

from cart.serializers import (CartItemSerializer,
                                CartSerializer,
                                )

class CartViewSet(ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    print("||||||||||||||||||")
    print(queryset)


class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = CartItem.objects.filter(cart__user=self.request.user).prefetch_related()
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>get_queryset")
        return queryset

    def update(self, request) -> Response:
        product_id = request.data["id"]
        count = request.data["count"]

        cart, created = Cart.objects.get_or_create(user=request.user)
        product = Product.objects.get(id=product_id)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.count += count

        cart_item.save()

        print("!!!!!!!!!!!!!!!!!!!!!!!!!create")
        print(product_id, count)

        cart_items = CartItem.objects.filter(cart=cart)
        serializer = self.get_serializer(cart_items, many=True)

        return Response(serializer.data, status=201)

    def list(self, request: Request) -> Response:
        data = self.get_serializer(self.get_queryset(), many=True).data
        print("!!!!!!!!!!!!!!!!!!!!!!!cart_list")
        return Response(data)

    def destroy(self, request, id):
        pass

