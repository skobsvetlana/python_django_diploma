from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from cart.models import Cart, CartItem
from order.models import Order, Address, City
from order.serializers.order_create_serializer import OrderSerializer
from order.serializers.order_update_serializer import OrderDetailSerializer

def filter_data(data):
    """
    Фильтрует данные, оставляя только ключи 'id', 'count', 'price' и переименовывает ключ 'id' в 'product'.

    :param data: Список словарей, содержащих данные.
    :return: Список словарей с отфильтрованными данными.
    """
    keys = ["id", "count", "price"]
    data = [{key: item.get(key, None) for key in keys} for item in data]

    for item in data:
        item["product"] = item.pop("id")

    return data


class OrderViewSet(ModelViewSet):
    """
    ViewSet для работы с заказами.
    """
    queryset = Order.objects.all()

    def get_serializer_class(self):
        """
        Возвращает сериализатор в зависимости от метода запроса.

        :return: Класс сериализатора.
        """
        if self.request.method == 'POST':
            return OrderSerializer
        elif self.request.method == 'GET':
            return OrderDetailSerializer


    def get_queryset(self):
        """
        Возвращает QuerySet заказов для текущего пользователя.

        :return: QuerySet заказов.
        """
        queryset = (
            Order.objects
            .select_related("customer", "address")
            .filter(customer=self.request.user)
        )
        return queryset


    def create(self, request, *args, **kwargs):
        """
        Создает новый заказ.

        :param request: Запрос на создание заказа.
        :param args: Дополнительные аргументы.
        :param kwargs: Дополнительные именованные аргументы.
        :return: Ответ с ID созданного заказа.
        """
        order_id = request.session.get('order_id')

        if order_id is not None:
            return Response(
                data={"orderId": order_id},
                status=status.HTTP_200_OK,
            )

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
        order_id = serializer.instance.pk
        request.session['order_id'] = order_id

        return Response(
            data={"orderId": order_id},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


    def perform_create(self, serializer):
        """
        Создание заказа и его связь с пользователем, если он зарегистрирован

        :param serializer: Сериализатор для создания заказа.
        """
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
        """
        Возвращает список заказов для текущего пользователя.

        :param request: Запрос на получение списка заказов.
        :param args: Дополнительные аргументы.
        :param kwargs: Дополнительные именованные аргументы.
        :return: Ответ с данными заказов.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

