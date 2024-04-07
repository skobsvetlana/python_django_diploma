from django.db import models

from catalog.models.product_model import Product


def product_images_directory_path(instance: "Images", filename: str) -> str:
    """
    Функция для определения пути сохранения изображений продуктов.

    :param instance: Экземпляр модели Images.
    :param filename: Имя файла изображения.
    :return: Строка с путем к директории для сохранения изображения.
    """
    return "products/product_{pk}/{filename}".format(
        pk=instance.product.pk,
        filename=filename
    )


class Images(models.Model):
    """
    Модель для хранения изображений продуктов.

    Атрибуты:
    - product: Ссылка на продукт, к которому относится изображение.
    - src: Поле для хранения изображения, использует функцию product_images_directory_path для определения пути сохранения.
    - alt: Альтернативный текст для изображения.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    src = models.ImageField(upload_to=product_images_directory_path)
    alt = models.CharField(max_length=200, null=False, blank=True)