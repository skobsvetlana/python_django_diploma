from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from catalog.serializers.review_serializer import ReviewsSerializer
from catalog.models.product_model import Review

class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.prefetch_related("author", "product",).all()
    serializer_class = ReviewsSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post', ]


    # def create(self, request, *args, **kwargs):
    #     print("55555555555555555555")
    #     product_id = request.data["id"]
    #     text = request.data["text"]
    #     email = request.data["text"]
    #     rate = request.data["text"]
    #     print(request.data)
    #     author = self.request.user
    #
    #     review, created = Review.objects.create(
    #         author=author,
    #         text=text,
    #         rate=rate,
    #         email=email,
    #         product=product_id)
    #
    #     review.save()
    #     serializer = self.get_serializer(data=review)
    #     serializer.is_valid(raise_exception=True)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

