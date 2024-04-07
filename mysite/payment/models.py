from django.db import models

from order.models import Order


class Payment(models.Model):
    """
    Модель для хранения информации о платежах. Связь с моделью Order. Определяет, к какому заказу относится платеж.
    """
    order = models.ForeignKey(Order, on_delete=models.PROTECT, null=False)
    number = models.CharField(null=False, max_length=16, blank=True, default="")
    name = models.CharField(max_length=100, blank=True, default="")
    month = models.CharField(null=False, max_length=2, blank=True, default="")
    year = models.CharField(null=False, max_length=4, blank=True, default="")
    code = models.CharField(null=False, max_length=3, blank=True, default="")

    def __str__(self):
        """
        Возвращает строковое представление объекта Payment.
        """
        return (f"name: {self.name}/n   "
                f"number: {self.number}/n   "
                f"month/year {self.month}/{self.year} code: {self.code}")

