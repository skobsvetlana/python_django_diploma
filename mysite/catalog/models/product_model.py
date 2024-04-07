from django.db import models
from django.contrib.auth.models import User

from catalog.models.category_model import Category

from catalog.models.tag_model import Tag

from catalog.models.specification_model import Specification

class Product(models.Model):
    """
    Модель продукта с различными атрибутами и связями.
    """
    class Meta:
        ordering = ["category", "title", "price"]

    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=False)
    title = models.CharField(null=False, max_length=100)
    price = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    totalCount = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    fullDescription = models.TextField(null=False, blank=True)
    limited_edition = models.BooleanField(default=False)
    free_delivery = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="tags")
    specifications = models.ManyToManyField(Specification, blank=True, related_name="specifications")

    @property
    def description(self) -> str:
        """
        Возвращает описание продукта, обрезанное до 50 символов, если оно превышает эту длину.
        """
        if len(self.fullDescription) < 50:
            return self.fullDescription
        else:
            return self.fullDescription[:50] + "..."

    @property
    def reviews_count(self):
        """
        Возвращает количество отзывов для данного продукта.
        """
        reviews = Review.objects.filter(product=self)
        if reviews:
            return reviews.count()
        return None

    @property
    def rating(self):
        """
        Вычисляет среднюю оценку отзывов для данного продукта.
        """
        rating = Review.objects.filter(product=self).aggregate(models.Avg('rate'))['rate__avg']
        if rating:
            rating = round(rating, 1)
        return rating

    def __str__(self) -> str:
        """
        Возвращает строковое представление продукта.
        """
        return self.title

    # def get_absolute_url(self):
    #     return reverse('catalog:product_detail', kwargs={'pk': self.pk})


class Review(models.Model):
    """
    Модель отзыва, связанная с продуктом.
    """
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.TextField(null=False, blank=True)
    rate = models.PositiveSmallIntegerField(null=False, blank=False, default=0)
    date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(null=True, blank=True)
    author = models.CharField(max_length=150, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=False, related_name="reviews")
