from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from order.models import Order
from payment.models import Payment
from payment.serializers import PaymentSerializer


class PaymentViewset(ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def create(self, request: Request, *args, **kwargs) -> Response:
        # order_id = self.request.session.get('order_id')
        # payment_id = self.request.session['payment_id']
        print(request.data)
        # try:
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
        # except:
        #     print("there is not payment data")


    def perform_create(self, serializer):
        # Создание платежа и его связь с заказом
        order_id = self.request.kwargs.get("id")
        order = Order.objects.get_object_or_404(pk=order_id)
        validated_data = serializer.validated_data
        validated_data['order'] = order
        print("perform_create validated_data", validated_data)
        serializer.save()


    # def retrieve(self, request: Request, *args, **kwargs) -> Response:
    #
    #     payment, created = Payment.objects.get_or_create(customer=request.user)
    #
    #     serializer = self.get_serializer(payment)
    #
    #     return Response(serializer.data)


