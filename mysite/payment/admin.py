from django.contrib import admin

from payment.models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'order',
        'number',
        'name',
        'month',
        'year',
        'code',
    ]
    list_display_links = "order", "number", "name",
    search_fields = "order", "number", "name",
