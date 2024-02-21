from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from django.shortcuts import get_object_or_404

from order.models import Order
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
            print("request.user.is_authenticated")
            data = request.data
            #Cart.objects.get(user=request.user).delete()
        else:
            print("request.user.is_not_authenticated")
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
        validated_data = serializer.validated_data
        if self.request.user.is_authenticated:
            print("request.user.is_authenticated")
            validated_data['customer'] = user
            validated_data['fullName'] = user.first_name
            validated_data['email'] = user.email
            validated_data['phone'] = user.profile.phone
        serializer.save()


    def list(self, request: Request, *args, **kwargs) -> Response:
        #queryset = self.filter_queryset(self.get_queryset())
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class OrderDetailViewSet(ModelViewSet):
    #permission_classes = [IsAuthenticated]
    serializer_class = OrderDetailSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['customer',]


    def get_queryset(self):
        queryset = (
            Order.objects
            .select_related("customer", "address")
            .filter(customer=self.request.user)
        )
        return queryset

    def uodate(self, request: Request, *args, **kwargs) -> Response:
        id = kwargs.get("pk")
        print(id)
        return Response()


    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        id = kwargs.get("pk")
        print(args, kwargs)
        item = get_object_or_404(self.queryset, pk=id)
        serializer = self.get_serializer(item)
        print("++++++++++++++++++++++++order_retrieve")
        print(serializer.data)
        return Response(serializer.data)


    def list(self, request: Request, *args, **kwargs) -> Response:
        #queryset = self.filter_queryset(self.get_queryset())
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)





