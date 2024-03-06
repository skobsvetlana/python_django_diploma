from django.contrib import admin

from order.models import (
    Order,
    OrderItem, DeliveryCost,
)

class OrderItemInline(admin.StackedInline):
    model = OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline,
    ]
    list_display = [
        "pk",
        "customer",
        "createdAt",
        "fullName",
        "email",
        "phone",
        "deliveryType",
        "paymentType",\
        "status",
        "address",
        "city",
        ]
    list_display_links = "pk", "createdAt", "customer",
    search_fields = "customer", "createdAt", "status",


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "order",
        "product",
        "count",
        ]
    list_display_links = "order", "product",
    search_fields = "order",  "product",


@admin.register(DeliveryCost)
class DeliveryCostAdmin(admin.ModelAdmin):
    list_display = [
        "ordinary",
        "express",
        "minCostForFreeDelivery",
        "dateFrom",
        "dateTo",
        ]

