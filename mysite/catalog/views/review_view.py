from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from catalog.serializers.review_serializer import ReviewsSerializer
from catalog.models.product_model import Review, Product


class ReviewViewSet(ModelViewSet):
    """
    ViewSet для работы с отзывами (Review).
    Предоставляет возможность создавать отзывы, связанные с определенным продуктом.
    """
    queryset = Review.objects.prefetch_related("author", "product",).all()
    serializer_class = ReviewsSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post', ]


    def create(self, request, *args, **kwargs):
        """
        Создает новый отзыв. Принимает данные отзыва, включая ID продукта и ID пользователя, и сохраняет
        их в базе данных.

        :param request: Запрос на создание отзыва.
        :param args: Дополнительные аргументы.
        :param kwargs: Дополнительные именованные аргументы.
        :return: Ответ с созданным отзывом и статусом 201 Created.
        """
        product_id = kwargs["id"]
        data = request.data
        user = self.request.user
        #product = Product.objects.get(pk=product_id)

        data["user"] = user.pk
        data["product"] = product_id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

