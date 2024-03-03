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

    def create(self):
        order_id = self.request.session.get('order_id')
        payment_id = self.request.session['payment_id']
        order = Order.objects.get(pk=order_id)

        if order is not None:

            payment_data = {
                'order': order,
            }
            payment = Payment.objects.create(**payment_data)

            return Response(
                data={"id": payment.pk},
                status=status.HTTP_200_OK,
            )





    def retrieve(self, request: Request, *args, **kwargs) -> Response:

        payment, created = Payment.objects.get_or_create(customer=request.user)

        serializer = self.get_serializer(payment)

        return Response(serializer.data)


