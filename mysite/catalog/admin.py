from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from catalog.models import (Product,
                            Category,
                            Tag,
                            Review,
                            Images,
                            Specification,
                            SaleItem,
                            )


@admin.action(description="limited_addition ON")
def limited_addition_on(modelAdmin: admin.ModelAdmin, request: HttpRequest, querryset: QuerySet):
    querryset.update(limited_edition=True)


@admin.action(description="limited_addition OFF")
def limited_addition_off(modelAdmin: admin.ModelAdmin, request: HttpRequest, querryset: QuerySet):
    querryset.update(limited_edition=False)


class TagInline(admin.TabularInline):
    model = Product.tags.through


class SpecificationInline(admin.TabularInline):
    model = Product.specifications.through


class ImagesInline(admin.StackedInline):
    model = Images


class SaleItemInline(admin.StackedInline):
    model = SaleItem


class ReviewInline(admin.StackedInline):
    model = Review


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = [
        limited_addition_on,
        limited_addition_off,
    ]
    inlines = [
        SaleItemInline,
        TagInline,
        ImagesInline,
        SpecificationInline,
        ReviewInline,
    ]
    list_display = ["pk",
                    "category",
                    "title",
                    "price",
                    "totalCount",
                    "description",
                    "free_delivery",
                    "limited_edition",
                    ]
    list_display_links = "pk", "title"
    ordering = "title", "pk",
    search_fields = "category", "title", "description",
    readonly_fields = ["date", ]
    classes = ["collapse"]


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = "id", "product", "salePrice", "dateFrom", "dateTo",
    list_display_links = "id", "product",


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "pk", "title", "parent", "src", "alt"
    list_display_links = "pk", "title"

    fieldsets = (
        ('Основная информация', {'fields': ('title', 'parent')}),
        ('Фотография', {'fields': ('src', 'alt',)})
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = "pk", "name"
    list_display_links = "pk", "name"


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = "pk", "name", "value"
    list_display_links = "pk", "name"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = "pk", "author", "product", "text", "rate", "date",
    list_display_links = "pk", "product", "text"
