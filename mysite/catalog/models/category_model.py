from rest_framework import serializers

from django.db import models

def category_image_directory_path(instance: "Category", filename: str) -> str:
    return "categories/category_{pk}/{filename}".format(
        pk=instance.pk,
        filename=filename
    )


class Category(models.Model):
    """
    Модель категорий с вложенностью
    """
    title = models.CharField(max_length=150, null=False)
    src = models.ImageField(default="pics/daisy.jpeg", upload_to=category_image_directory_path)
    alt = models.CharField(max_length=200, null=False, blank=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        db_index=True,
        related_name="subcategories",
    )

    @property
    def image(self):
        return {'src': serializers.ImageField().to_representation(self.src),
                'alt': self.alt,
                }

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title