from rest_framework import serializers

from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


    def create(self, validated_data):
        payment = Payment.objects.create(**validated_data)
        print("payment **validated_data", **validated_data)
        return payment
