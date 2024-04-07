from catalog.models.product_model import Review

from rest_framework import serializers

class ReviewsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Review.
    Предоставляет методы для создания, валидации и представления объектов Review.
    """
    class Meta:
        model = Review
        fields = '__all__'


    def create(self, validated_data):
        """
       Создает новый объект Review с валидированными данными.

       :param validated_data: Валидированные данные для создания объекта Review.
       :return: Созданный объект Review.
       """
        review = Review.objects.create(**validated_data)

        return review

    def validate(self, data):
        """
        Валидирует данные перед созданием объекта Review.
        Проверяет, что пользователь еще не оставлял отзыв на данный продукт.

        :param data: Данные для создания объекта Review.
        :return: Валидированные данные.
        :raises serializers.ValidationError: Если пользователь уже оставлял отзыв на данный продукт.
        """
        product = data.get('product')
        user = self.context['request'].user

        if Review.objects.filter(product=product, user=user).exists():
            raise serializers.ValidationError("This user has already added a review for this product.")

        return data

    def to_representation(self, instance):
        """
        Переопределение метода для изменения представления данных отзыва на товар.
        Если поле author не заполнено, то имя автора отзыва заменяется на сообщение "Пользователь предпочёл
        скрыть свои данные".
        :param instance: Объект Review.
        :return: Словарь с данными объекта Review.
        """
        data = super().to_representation(instance)
        if data["author"] == "":
            data["author"] = "Пользователь предпочёл скрыть свои данные"

        return data
у4