from django.db import models


class Specification(models.Model):
    """
    Модель для хранения спецификаций товаров.
    """

    class Meta:
        ordering = ["name"]  # Сортировка по умолчанию по полю name

    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        """
        Возвращает строковое представление объекта Specification.

        :return: Название категории, значение спецификации.
        """
        return f'{self.name}    {self.value}'
