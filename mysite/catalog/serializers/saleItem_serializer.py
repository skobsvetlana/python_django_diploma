from catalog.models.saleItem_model import SaleItem

from rest_framework import serializers

from catalog.serializers.image_serializer import ImagesSerializer


class SaleItemSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(required=False, source="product.images", many=True)
    id = serializers.CharField(source='product.id')
    price = serializers.FloatField(source='product.price')
    title = serializers.CharField(source='product.title')
    salePrice = serializers.SerializerMethodField(method_name="get_salePrice")
    dateFrom = serializers.SerializerMethodField(method_name="get_dateFrom")
    dateTo = serializers.SerializerMethodField(method_name="get_dateTo")

    class Meta:
        model = SaleItem
        fields = [
            "id",
            "price",
            "salePrice",
            "dateFrom",
            "dateTo",
            "title",
            "images",
        ]

    def get_salePrice(self, item: SaleItem):
        return float(item.salePrice)

    def get_dateFrom(self, item: SaleItem):
        return item.dateFrom.strftime("%a %b %d %Y %H:%M:%S GMT%z %Z")

    def get_dateTo(self, item: SaleItem):
        return item.dateTo.strftime("%a %b %d %Y %H:%M:%S GMT%z %Z")
