from django.db import models
from django.contrib.auth.models import User

from catalog.models import Product


class Order(models.Model):
    class Meta:
        ordering = ('-createdAt',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pk

    # def get_total_cost(self):
    #     return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_item')
    count = models.PositiveIntegerField(null=False)
    price = models.DecimalField(null=False, max_digits=10, decimal_places=2)

    def __str__(self):
        return '{}'.format(self.pk)

    # def get_cost(self):
    #     return self.product.price * self.count


class Address(models.Model):
    class Meta:
        verbose_name = "Shipping Address"
        verbose_name_plural = "Shipping Addresses"

    address1 = models.CharField(
        "Address line 1",
        null=False,
        blank=True,
        max_length=1024,
    )

    address2 = models.CharField(
        "Address line 2",
        max_length=1024,
        blank=True,
        default="",
    )

    zip_code = models.CharField(
        "ZIP / Postal code",
        max_length=12,
    )

    city = models.CharField(
        "City",
        null=False,
        max_length=1024,
    )

    def __str__(self):
        return f"{self.address1}, unit {self.address2}, {self.city}, {self.zip_code}"


class OrderDetails(models.Model):
    class Status(models.TextChoices):
        CREATED = 'created',
        PAID = 'paid',
        ACCEPTED = 'accepted',


    class PaymentType(models.TextChoices):
        CARD = 'card',
        RANDOM_ACCOUNT = 'random account',


    customer = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    paymentType = models.CharField(
        max_length=20,
        choices=PaymentType.choices,
        default=PaymentType.CARD,
    )
    #totalCost = models.DecimalField(null=False, max_digits=12, decimal_places=2, default=0)
    status =models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CREATED,
    )
    address = models.ForeignKey(Address, on_delete=models.PROTECT, null=True)
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return 'Order №{number} status {status}'.format(
            number=self.order,
            status=self.status
        )




