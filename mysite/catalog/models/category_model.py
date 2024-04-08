from rest_framework import serializers

from django.db import models

def category_image_directory_path(instance: "Category", filename: str) -> str:
    """
    Функция для определения пути сохранения изображения категории.

    :param instance: Экземпляр модели Category.
    :param filename: Имя файла изображения.
    :return: Строка с путем к директории для сохранения изображения.
    """
    return "categories/category_{pk}/{filename}".format(
        pk=instance.pk,
        filename=filename
    )


class Category(models.Model):
    """
    Модель категорий с вложенностью

    Атрибуты:
    - title: Название категории.
    - src: Изображение категории.
    - alt: Альтернативный текст для изображения.
    - parent: Ссылка на родительскую категорию.

    Методы:
    - image: Свойство, возвращающее словарь с информацией об изображении.
    """
    title = models.CharField(max_length=150, null=False)
    src = models.ImageField(default="pics/daisy.jpeg", upload_to=category_image_directory_path)
    alt = models.CharField(max_length=200, null=False, blank=True)
    banner = models.BooleanField(default=False)
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
        """
        Свойство, возвращающее словарь с информацией об изображении категории.

        :return: Словарь с ключами 'src' и 'alt'.
        """
        return {'src': serializers.ImageField().to_representation(self.src),
                'alt': self.alt,
                }

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        """
        Возвращает строковое представление объекта Category.

        :return: Название категории.
        """
        return self.title