from rest_framework import serializers

from payment.models import Payment

def validate_card_number(number):
    if len(number) > 16:
        raise serializers.ValidationError("Card number must not be longer than 16 digits.")
    if int(number) % 2 != 0 or int(number[-2:-1]) == 0:
        raise serializers.ValidationError("Card number must be even and last digit must be more than 0.")
    return number


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        extra_kwargs = {
            'number': {'validators': [validate_card_number]},
        }


    def create(self, validated_data):
        payment = Payment.objects.create(**validated_data)
        return payment
