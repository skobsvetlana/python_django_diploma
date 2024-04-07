from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from django.shortcuts import get_object_or_404

from order.models import Order, Address, City
from order.serializers.order_update_serializer import OrderDetailSerializer


class OrderDetailViewSet(ModelViewSet):
    """
    ViewSet для работы с деталями заказа.
    Предоставляет методы для просмотра, обновления и извлечения информации о заказах.
    """
    permission_classes = [IsAuthenticated]
    queryset = (Order.objects
                .prefetch_related("customer", "address", "city", )
                .all()
                )
    serializer_class = OrderDetailSerializer


    def update(self, request: Request, *args, **kwargs):
        """
        Обновляет информацию о заказе.
        Проверяет, что заказ еще не оплачен и обновляет его статус на 'accepted'.
        Если заказ не имеет клиента, устанавливает текущего пользователя в качестве клиента.
        """
        id = kwargs.get("id")
        instance = get_object_or_404(self.queryset, pk=id)

        if instance.status == "paid":
            raise ValueError(
                    f"Order №{id} is already paid.")

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
        order_id = serializer.instance.pk

        return Response(
            data={"orderId": order_id},
            status=status.HTTP_200_OK
        )


    def perform_update(self, serializer):
        """
        Выполняет обновление заказа, создавая или обновляя связанные объекты City и Address.
        """
        validated_data = serializer.validated_data
        city, created = City.objects.get_or_create(name=validated_data['city'].upper())
        address, created = Address.objects.get_or_create(address1=validated_data['address'].upper())
        validated_data['city'] = city
        validated_data['address'] = address
        serializer.save()


    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        """
        Извлекает информацию о заказе по его идентификатору.
        Использует идентификатор из URL или из сессии, если он не указан в URL.
        """
        try:
            order_id = kwargs.get("id")
        except TypeError:
            order_id = request.session.get('order_id')

        instance = get_object_or_404(self.queryset, pk=order_id)
        serializer = self.get_serializer(instance)

        return Response(serializer.data)
