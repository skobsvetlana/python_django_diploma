from django.contrib.auth.models import User

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from django.shortcuts import get_object_or_404

from order.models import Order, Address, City
from order.serializers.order_update_serializer import OrderDetailSerializer


class OrderDetailViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = (Order.objects
                .prefetch_related("customer", "address", "city", )
                .all()
                )
    serializer_class = OrderDetailSerializer

    def update(self, request: Request, *args, **kwargs) -> Response:
        print("++++++++++++++++++++++++order_update")
        id = kwargs.get("id")
        print(id)
        instance = get_object_or_404(self.queryset, pk=id)

        if instance.customer == None:
            user = User.objects.get(pk=request.user.pk)
            instance.customer = user

        instance.status = 'accepted'
        serializer = self.get_serializer(
            instance=instance,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            data=serializer.data,
            status=status.HTTP_202_ACCEPTED,
        )

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
