from django.db import models
from django.contrib.auth.models import User

from catalog.models.product_model import Product

import uuid

class Cart(models.Model):
    #id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart", null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="cart_item", null=True, blank=True)
    count = models.PositiveIntegerField(default=0)

