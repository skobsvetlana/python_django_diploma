from collections import OrderedDict

from rest_framework import pagination, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from catalog.serializers import SaleItemSerializer

from catalog.models import SaleItem

class SalesViewSet(ModelViewSet):
    queryset = (
        SaleItem.objects.select_related("product").all()
    )
    serializer_class = SaleItemSerializer