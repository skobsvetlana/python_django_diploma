from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from django.shortcuts import get_object_or_404

from cart.models import Cart, CartItem
from order.models import Order
from order.serialisers import OrderSerializer

def filter_data(data):
    keys = ["id", "count", "price"]
    data = [{key: item.get(key, None) for key in keys} for item in data]

    for item in data:
        item["product"] = item.pop("id")

    return data


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    #permission_classes = [IsAuthenticatedOrReadOnly]

    def retrieve(self, request: Request, id, *args, **kwargs) -> Response:
        item = get_object_or_404(self.queryset, pk=id)
        serializer = self.get_serializer(item)
        print("++++++++++++++++++++++++order_retrieve")
        return Response(serializer.data)


    def list(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print("request.user.is_authenticated")
            data = request.data
            Cart.objects.get(user=request.user).delete()
        else:
            print("request.user.is_not_authenticated")
            data = request.session.get('cart_data', [])
            request.session['cart_data'] = []

        data = filter_data(data)

        serializer = self.get_serializer(data={"items": data})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)


        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )


    def perform_create(self, serializer):
        # Создание заказа и связывание его с пользователем, если он зарегистрирован
        serializer.save(customer=self.request.user if self.request.user.is_authenticated else None)




