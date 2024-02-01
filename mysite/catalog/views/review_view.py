from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from catalog.serializers import ReviewsSerializer

from catalog.models import Review

class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewsSerializer

    def create(self, request, *args, **kwargs):
        pass