from django.db import models

class Tag(models.Model):
    """
    Модель тега, используемая для категоризации или тегирования объектов.
    """
    class Meta:
        ordering = ["name"]

    name = models.CharField(null=False, max_length=100)

    def __str__(self):
        """
        Возвращает строковое представление объекта тега.

        Возвращает:
            str: Название тега.
        """
        return f'{self.name}'