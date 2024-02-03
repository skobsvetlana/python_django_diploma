from django.contrib import admin

from profiles.models import Profile

@admin.register(Profile)
class CartAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "phone",
        "src",
        "alt",
        ]
    list_display_links = "user",
    search_fields = "user",