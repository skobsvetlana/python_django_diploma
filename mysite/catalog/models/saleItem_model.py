from django.db import models

from django.utils.timezone import now

from catalog.models.product_model import Product


class SaleItem(models.Model):
    """
    Модель предложения товара со скидкой.
    """
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    salePrice = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    dateFrom = models.DateTimeField(default=now)
    dateTo = models.DateTimeField(null=True)
