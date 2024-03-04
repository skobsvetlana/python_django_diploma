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
        order_id = kwargs.get("id")
        data = request.data
        data["order"] = order_id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        order = Order.objects.get(pk=order_id)
        order.status = "paid"
        order.save()
        request.session['order_id'] = None

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )



