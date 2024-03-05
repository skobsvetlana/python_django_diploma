from django.db import models

from catalog.models.product_model import Product


def product_images_directory_path(instance: "Images", filename: str) -> str:
    return "products/product_{pk}/{filename}".format(
        pk=instance.product.pk,
        filename=filename
    )


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    src = models.ImageField(upload_to=product_images_directory_path)
    alt = models.CharField(max_length=200, null=False, blank=True)