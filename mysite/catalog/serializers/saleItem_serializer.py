from catalog.models.saleItem_model import SaleItem

from rest_framework import serializers

from catalog.serializers.image_serializer import ImagesSerializer


class SaleItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для объектов SaleItem, включает в себя информацию о продукте,
    его изображения, цену, акционную цену, даты начала и окончания акции.
    """
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
        """
        Возвращает акционную цену товара.
        """
        return float(item.salePrice)

    def get_dateFrom(self, item: SaleItem):
        """
        Возвращает дату начала акции в формате строки.
        """
        return item.dateFrom.strftime("%a %b %d %Y %H:%M:%S GMT%z %Z")

    def get_dateTo(self, item: SaleItem):
        """
        Возвращает дату окончания акции в формате строки.
        """
        return item.dateTo.strftime("%a %b %d %Y %H:%M:%S GMT%z %Z")
