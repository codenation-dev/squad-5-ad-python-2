from rest_framework import serializers
from .models import Comissions, Sellers


class ComissionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comissions
        fields = ('id', 'lower_percentage', 'min_value', 'upper_percentage')

    # def validate_lower_percentage(self, value):
    #     """
    #     Check that value is a valid name.
    #     """
    #     if value is None:  # check name has more than 1 word
    #         raise serializers.ValidationError(
    #             "Número Pequeno")  # raise ValidationError
    #     return value


class SellersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sellers
        fields = ('id', 'name', 'address', 'phone', 'age',
                  'email', 'cpf', 'comission')
