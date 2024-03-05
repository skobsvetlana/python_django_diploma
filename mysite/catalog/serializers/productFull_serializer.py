from rest_framework import serializers

from catalog.models.product_model import Product
from catalog.models.saleItem_model import SaleItem
from catalog.serializers.image_serializer import ImagesSerializer
from catalog.serializers.review_serializer import ReviewsSerializer
from catalog.serializers.specification_serializer import SpecificationsSerializer
from catalog.serializers.tag_serializer import TagSerializer


class ProductFullSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True, required=False)
    reviews = ReviewsSerializer(many=True, required=False)
    specifications = SpecificationsSerializer(many=True, required=False)
    tags = TagSerializer(many=True, required=False)
    count = serializers.SerializerMethodField(method_name="get_count")
    price = serializers.SerializerMethodField(method_name="get_price")
    date = serializers.SerializerMethodField(method_name="date_to_string")

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "fullDescription",
            "free_delivery",
            "images",
            "tags",
            "reviews",
            "specifications",
            "rating",
        ]

    def get_count(self, product: Product):
        return product.totalCount

    def get_price(self, product: Product):
        return float(product.price)

    def date_to_string(self, product: Product):
        return product.date.strftime("%a %b %d %Y %H:%M:%S GMT%z %Z")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        sale_item = SaleItem.objects.filter(product=instance.pk).first()

        if sale_item:
            data['price'] = float(sale_item.salePrice)

        return data
