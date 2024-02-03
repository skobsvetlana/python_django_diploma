from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.timezone import now


def product_images_directory_path(instance: "Images", filename: str) -> str:
    return "images/products/product_{pk}/{filename}".format(
        pk=instance.product.pk,
        filename=filename
    )

def category_image_directory_path(instance: "Category", filename: str) -> str:
    return "images/categories/category_{pk}/{filename}".format(
        pk=instance.pk,
        filename=filename
    )

class Category(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    title = models.CharField(max_length=150, null=False)
    src = models.ImageField(default="pics/daisy.jpeg", upload_to=category_image_directory_path)
    alt = models.CharField(max_length=200, null=False, blank=True)
    category_id = models.PositiveIntegerField(default=0)

    @property
    def image(self):
        return {'src': self.src,
                'alt': self.alt,
                }

    def __str__(self):
        return f'{self.title}'


class Tag(models.Model):
    name = models.CharField(null=False, max_length=100)

    def __str__(self):
        return f'{self.name}'


class Specification(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}    {self.value}'


class Product(models.Model):
    class Meta:
        ordering = ["title", "price"]

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
        if len(self.fullDescription) < 50:
            return self.fullDescription
        else:
            return self.fullDescription[:50] + "..."

    @property
    def reviews_count(self):
        reviews = Review.objects.filter(product=self)
        if reviews:
            return reviews.count()
        return None

    @property
    def rating(self):
        rating = Review.objects.filter(product=self).aggregate(models.Avg('rate'))['rate__avg']
        if rating:
            rating = round(rating, 1)
        return rating

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('shopapp:product_detail', kwargs={'pk': self.pk})


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.TextField(null=False, blank=True)
    rate = models.PositiveSmallIntegerField(null=False, blank=False, default=0)
    date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=False, related_name="reviews")


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    src = models.ImageField(upload_to=product_images_directory_path)
    alt = models.CharField(max_length=200, null=False, blank=True)


class SaleItem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    salePrice = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    dateFrom = models.DateTimeField(default=now)
    dateTo = models.DateTimeField(null=True)















