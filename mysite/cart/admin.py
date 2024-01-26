from django.contrib import admin
from  django.db.models import QuerySet
from django.http import HttpRequest
from django.contrib.auth.models import User
from cart.models import (Product,
                     Cart,
                     CartItem,
                     )

class CartItemInline(admin.StackedInline):
    model = CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [
        CartItemInline,
    ]
    list_display = [
        "pk",
        "user",
        "createdAt",
        ]
    list_display_links = "pk", "createdAt",
    #search_fields = "product",


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "cart",
        "product",
        "count",
        ]
    list_display_links = "cart", "product",
    #search_fields = "product",











