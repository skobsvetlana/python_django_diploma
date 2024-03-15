from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from catalog.serializers.review_serializer import ReviewsSerializer
from catalog.models.product_model import Review, Product


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.prefetch_related("author", "product",).all()
    serializer_class = ReviewsSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post', ]


    def create(self, request, *args, **kwargs):
        product_id = kwargs["id"]
        data = request.data
        user = self.request.user
        #product = Product.objects.get(pk=product_id)

        if data["author"] == "":
            data["author"] = "Anonymous"

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

