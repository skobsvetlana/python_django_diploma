from rest_framework import serializers

from payment.models import Payment

def validate_card_number(number):
    """
    Проверяет, соответствует ли номер карты определенным условиям.

    :param number: Номер карты в виде строки.
    :return: Номер карты, если он прошел валидацию.
    :raises serializers.ValidationError: Если номер карты не соответствует условиям.
    """
    if len(number) > 16:
        raise serializers.ValidationError("Card number must not be longer than 16 digits.")
    if int(number) % 2 != 0 or int(number[-2:-1]) == 0:
        raise serializers.ValidationError("Card number must be even and last digit must be more than 0.")
    return number


class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Payment.
    Использует валидатор validate_card_number для проверки номера карты.
    """
    class Meta:
        model = Payment
        fields = '__all__'
        extra_kwargs = {
            'number': {'validators': [validate_card_number]},
        }


    def create(self, validated_data):
        """
        Создает новый объект Payment с валидированными данными.

        :param validated_data: Валидированные данные для создания объекта Payment.
        :return: Созданный объект Payment.
        """
        payment = Payment.objects.create(**validated_data)
        return payment
