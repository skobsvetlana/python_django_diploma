from rest_framework_recursive.fields import RecursiveField

from catalog.models import (Product,
                            Tag,
                            Category,
                            Images,
                            SaleItem,
                            Review,
                            Specification,
                            )

from django.contrib.auth.models import User

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
        ]


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = [
            "src",
            "alt",
        ]


class ReviewsSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False)

    class Meta:
        model = Review
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            "id",
            "name",
        ]


class SpecificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = [
            "name",
            "value",
        ]


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


class ProductShortSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "price",
            "images",
        ]


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


class CatalogItemSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True, required=True)
    tags = TagSerializer(many=True, required=False)
    count = serializers.SerializerMethodField(method_name="get_count")
    price = serializers.SerializerMethodField(method_name="get_price")
    freeDelivery = serializers.SerializerMethodField(method_name="get_freeDelivery")
    date = serializers.SerializerMethodField(method_name="date_to_string")
    reviews = serializers.SerializerMethodField(method_name="get_reviews")

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
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "rating",
        ]

    def get_count(self, product: Product):
        return product.totalCount

    def get_price(self, product: Product):
        return float(product.price)

    def date_to_string(self, product: Product):
        return product.date.strftime("%a %b %d %Y %H:%M:%S GMT%z %Z")

    def get_freeDelivery(self, product: Product):
        return product.free_delivery

    def get_reviews(self, product: Product):
        return product.reviews_count

    def to_representation(self, instance):
        data = super().to_representation(instance)
        sale_item = SaleItem.objects.filter(product=instance.pk).first()

        if sale_item:
            data['price'] = float(sale_item.salePrice)

        return data


class CategorySerializer(serializers.ModelSerializer):
    subcategories = RecursiveField(allow_null=True, many=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "title",
            "image",
            "subcategories",
        ]

