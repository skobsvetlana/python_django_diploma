from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from django.shortcuts import get_object_or_404

from catalog.models import Product
from order.models import (
    Order,
    OrderItem
)

from order.serialisers import (
    OrderItemSerializer,
    OrderSerializer,
)


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.prefetch_related("product").all()

    def retrieve(self, request: Request, id, *args, **kwargs) -> Response:
        item = get_object_or_404(self.queryset, pk=id)
        serializer = self.get_serializer(item)
        print("++++++++++++++++++++++++order_retrieve")
        return Response(serializer.data)


    def list(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)


    def create(self):
        pass


class OrderItemViewSet(ModelViewSet):
    serializer_class = OrderItemSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = OrderItem.objects.filter(order__customer=self.request.user).prefetch_related()
        return queryset

    def create(self, request: Request, *args, **kwargs) -> Response:
        order_items = request.data
        request.session['order_items'] = order_items
        serializer = self.get_serializer(order_items, many=True)
        #print(serializer.data)
        # product_id = request.data["id"]
        # count = request.data["count"]
        # price = request.data["price"]
        #
        # order = Order.objects.create(customer=request.user)
        # product = Product.objects.get(id=product_id)

        # cart_items, created = CartItem.objects.get_or_create(corder=order, product=product)
        # order.count = int(count)
        # order.pr
        #
        # cart_item.save()
        #
        # cart_items = CartItem.objects.filter(cart=cart)
        # serializer = self.get_serializer(cart_items, many=True)
        #
        return Response(serializer.data, status=status.HTTP_200_OK)


    # # def list(self, request: Request, *args, **kwargs) -> Response:
    # #     serializer = self.get_serializer(self.get_queryset(), many=True)
    # #     return Response(serializer.data)


    # def destroy(self, request: Request, *args, **kwargs):
    #     product_id = request.data["id"]
    #     count = request.data["count"]
    #
    #     cart, created = Cart.objects.get_or_create(user=request.user)
    #     product = Product.objects.get(id=product_id)
    #
    #     cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    #
    #     if cart_item.count > count:
    #         cart_item.count -= count
    #         cart_item.save()
    #     else:
    #         cart_item.delete()
    #
    #     cart_items = CartItem.objects.filter(cart=cart)
    #     serializer = self.get_serializer(cart_items, many=True)
    #
    #     return Response(serializer.data, status=status.HTTP_200_OK)