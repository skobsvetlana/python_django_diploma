from django.contrib.auth import login
from django.contrib.auth.models import User

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from django.shortcuts import get_object_or_404

from cart.models import Cart, CartItem
from my_auth.serializers import UserRegistrationSerializer
from order.models import Order, Address, City
from order.serialisers import (
    OrderSerializer,
    OrderDetailSerializer,
)


def filter_data(data):
    keys = ["id", "count", "price"]
    data = [{key: item.get(key, None) for key in keys} for item in data]

    for item in data:
        item["product"] = item.pop("id")
        print(item["product"])

    return data


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderSerializer
        elif self.request.method == 'GET':
            return OrderDetailSerializer


    def get_queryset(self):
        queryset = (
            Order.objects
            .select_related("customer", "address")
            .filter(customer=self.request.user)
        )
        return queryset


    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            data = request.data
            cart = Cart.objects.get(user=request.user)
            CartItem.objects.filter(cart=cart).delete()
        else:
            data = request.session.get('cart_data', [])
            request.session['cart_data'] = []

        data = filter_data(data)
        serializer = self.get_serializer(data={"products": data})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            data={"orderId": serializer.instance.pk},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


    def perform_create(self, serializer):
        # Создание заказа и его связь с пользователем, если он зарегистрирован
        user = self.request.user
        city, created = City.objects.get_or_create(name="")
        address, created = Address.objects.get_or_create(
            address1="",
            address2="",
            zip_code="",
        )
        validated_data = serializer.validated_data

        if self.request.user.is_authenticated:
            validated_data['customer'] = user
            validated_data['fullName'] = user.first_name
            validated_data['email'] = user.email
            validated_data['phone'] = user.profile.phone
        validated_data['city'] = city
        validated_data['address'] = address
        serializer.save()


    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class OrderDetailViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = (Order.objects
                .prefetch_related("customer", "address", "city",)
                .all()
                )
    serializer_class = OrderDetailSerializer


    def update(self, request: Request, *args, **kwargs) -> Response:
        print("++++++++++++++++++++++++order_update")
        id = kwargs.get("id")
        instance = get_object_or_404(self.queryset, pk=id)
        instance.status = 'accepted'
        if instance.customer == None:
            user = User.objects.get(pk=request.user.pk)
            instance.customer = user

        serializer = self.get_serializer(
            instance=instance,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, )


    def perform_update(self, serializer):
        validated_data = serializer.validated_data
        city, created = City.objects.get_or_create(name=validated_data['city'].upper())
        address, created = Address.objects.get_or_create(address1=validated_data['address'].upper())
        validated_data['city'] = city
        validated_data['address'] = address
        serializer.save()


    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        print("+++++++++++retrieve")
        print("request.user.pk", request.user.pk)
        id = kwargs.get("id")
        instance = get_object_or_404(self.queryset, pk=id)
        if instance.customer == None:
            user = User.objects.get(pk=request.user.pk)
            instance.customer = user

            # instance.fullName = user.first_name
            # instance.email = user.email
            # instance.phone = user.profile.phone

        serializer = self.get_serializer(instance)

        return Response(serializer.data)
