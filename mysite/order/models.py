from django.db import models

from django.contrib.auth.models import User

from catalog.models.product_model import Product


class DeliveryCost(models.Model):
    """
    Модель для хранения стоимости доставки.

    Атрибуты:
    - ordinary: Стоимость обычной доставки.
    - express: Стоимость экспресс-доставки.
    - minCostForFreeDelivery: Минимальная стоимость заказа, при которой доставка бесплатна.
    - dateFrom: Дата начала действия стоимости доставки.
    - dateTo: Дата окончания действия стоимости доставки.
    """
    ordinary = models.DecimalField(null=False, max_digits=10, decimal_places=2, default=0)
    express = models.DecimalField(null=False, max_digits=10, decimal_places=2, default=0)
    minCostForFreeDelivery = models.DecimalField(null=False, max_digits=10, decimal_places=2, default=0)
    dateFrom = models.DateTimeField(auto_now_add=True)
    dateTo = models.DateTimeField(null=True, blank=True, default=None)


class City(models.Model):
    """
    Модель для хранения информации о городах.

    Атрибуты:
    - name: Название города.
    """
    name = models.CharField(
        null=False,
        blank=True,
        max_length=1024,
    )

    def __str__(self):
        return self.name


class Address(models.Model):
    """
    Модель для хранения информации об адресах доставки.

    Атрибуты:
    - address1: Первая строка адреса.
    - address2: Вторая строка адреса.
    - zip_code: Почтовый индекс.
    """
    class Meta:
        verbose_name = "Shipping Address"
        verbose_name_plural = "Shipping Addresses"

    address1 = models.CharField(
        "Address line 1",
        null=False,
        blank=True,
        max_length=1024,
    )
    address2 = models.CharField(
        "Address line 2",
        max_length=1024,
        blank=True,
        default="",
    )
    zip_code = models.CharField(
        "ZIP / Postal code",
        max_length=12,
    )


    def __str__(self):
        return f"{self.address1}, unit {self.address2}, {self.zip_code}"


class Order(models.Model):
    """
    Модель для хранения информации о заказах.

    Атрибуты:
    - createdAt: Дата и время создания заказа.
    - customer: Ссылка на пользователя, сделавшего заказ.
    - fullName: Полное имя клиента.
    - email: Электронная почта клиента.
    - phone: Телефон клиента.
    - deliveryType: Тип доставки.
    - paymentType: Тип оплаты.
    - status: Статус заказа.
    - address: Ссылка на адрес доставки.
    - city: Ссылка на город доставки.
    """
    class Status(models.TextChoices):
        """
        Этот класс определяет возможные статусы заказа. Каждый статус представлен в виде пары ключ-значение,
        где ключ - это имя статуса, а значение - это строка, которая будет сохраняться в базе данных.
        """
        CREATED = 'created',
        PAID = 'paid',
        ACCEPTED = 'accepted',
        COMPLETED = 'completed',


    class PaymentType(models.TextChoices):
        """
        Этот класс определяет типы оплаты заказа.
        """
        CARD = 'online',
        RANDOM_ACCOUNT = 'someone',


    class DeliveryType(models.TextChoices):
        """
        Этот класс определяет типы доставки заказа.
        """
        ORDINARY = 'ordinary',
        EXPRESS = 'express',


    class Meta:
        ordering = ('-createdAt',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    createdAt = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(User, on_delete=models.PROTECT, null=True, default=None)
    fullName = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    deliveryType = models.CharField(
        max_length=10,
        choices=DeliveryType.choices,
        default=DeliveryType.ORDINARY,
    )
    paymentType = models.CharField(
        max_length=20,
        choices=PaymentType.choices,
        default=PaymentType.CARD,
    )
    status =models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CREATED,
    )
    address = models.ForeignKey(Address, on_delete=models.PROTECT, null=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT, null=True)


    def __str__(self):
        """
        Возвращает строковое представление объекта заказа.

        Возвращает строку, содержащую номер заказа и его статус.

        Returns:
            str: Строка вида 'Order №{number} status {status}', где {number} - номер заказа,
                {status} - статус заказа.
        """
        return 'Order №{number} status {status}'.format(
            number=self.pk,
            status=self.status,
        )

    @property
    def totalCost(self):
        """
        Вычисляет общую стоимость заказа.

        Складывает стоимость всех товаров в заказе.

        Returns:
            float: Общая стоимость заказа.
        """
        total = sum(item.get_cost() for item in self.products.all())
        return total if total is not None else 0


    @property
    def deliveryCost(self):
        """
        Вычисляет стоимость доставки заказа.

        Стоимость доставки зависит от общей стоимости заказа и выбранного типа доставки.

        Returns:
            float: Стоимость доставки заказа.
        """
        delivery = 0
        delivery_costs = DeliveryCost.objects.order_by("-dateFrom").first()

        if self.totalCost < delivery_costs.minCostForFreeDelivery:
            delivery = delivery_costs.ordinary

        if self.deliveryType == "express":
            delivery += delivery_costs.express

        return delivery


    # @property
    # def totalCost(self):
    #     total = self.products.aggregate(total_cost=Sum(F('price') * F('count')))['total_cost']
    #     return total if total is not None else 0


class OrderItem(models.Model):
    """
    Модель для хранения информации о товарах в заказе.

    Атрибуты:
    - order: Ссылка на заказ.
    - product: Ссылка на товар.
    - count: Количество товара в заказе.
    - price: Цена товара.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_item')
    count = models.PositiveIntegerField(null=False)
    price = models.DecimalField(null=False, max_digits=10, decimal_places=2)

    def __str__(self):
        return '{}'.format(self.pk)

    def get_cost(self):
        return self.price * self.count





