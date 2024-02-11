# from django.db import models
# from django.contrib.auth.models import User
#
# from catalog.models import Product
#
# class Address(models.Model):
#     class Meta:
#         verbose_name = "Shipping Address"
#         verbose_name_plural = "Shipping Addresses"
#
#     address1 = models.CharField(
#         "Address line 1",
#         null=False,
#         blank=True,
#         max_length=1024,
#     )
#
#     address2 = models.CharField(
#         "Address line 2",
#         max_length=1024,
#     )
#
#     zip_code = models.CharField(
#         "ZIP / Postal code",
#         max_length=12,
#     )
#
#     city = models.CharField(
#         "City",
#         null=False,
#         max_length=1024,
#     )
#
#     def __str__(self):
#         return f"{self.address1}, unit {self.address2}, {self.city}, {self.zip_code}"
#
#
# class Order(models.Model):
#     customer = models.ForeignKey(User, on_delete=models.PROTECT)
#     class Status(models.TextChoices):
#         CREATED = 'created',
#         PAID = 'paid',
#         ACCEPTED = 'accepted',
#
#     createdAt = models.DateTimeField(auto_now_add=True)
#     #paymentType = models.ForeignKey(Payment, on_delete=models.PROTECT, null=False)
#     totalCost = models.DecimalField(null=False, max_digits=12, decimal_places=2, default=0)
#     status =models.CharField(
#         max_length=20,
#         choices=Status.choices,
#         default=Status.CREATED,
#     )
#     address = models.ForeignKey(Address, on_delete=models.PROTECT, null=False)
#
#     class Meta:
#         ordering = ('-createdAt',)
#         verbose_name = 'Order'
#         verbose_name_plural = 'Orders'
#
#     def __str__(self):
#         return 'Order №{} status {}'.format(self.pk, self.status)
#
#     # def get_total_cost(self):
#     #     return sum(item.get_cost() for item in self.items.all())
#
#
# class OrderProduct(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order')
#     product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
#     count = models.PositiveIntegerField(default=1)
#
#     def __str__(self):
#         return '{}'.format(self.pk)
#
#     # def get_cost(self):
#     #     return self.product.price * self.count
#
