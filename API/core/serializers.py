from rest_framework import serializers
from .models import Comissions, Sellers, Month_Comissions


class ComissionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comissions
        fields = ('id', 'lower_percentage', 'min_value', 'upper_percentage')


class SellersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sellers
        fields = ('id', 'name', 'address', 'phone',
                  'age', 'email', 'cpf', 'comission')


class Month_ComissionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Month_Comissions
        fields = ('id', 'id_seller', 'amount', 'month', 'comission')
