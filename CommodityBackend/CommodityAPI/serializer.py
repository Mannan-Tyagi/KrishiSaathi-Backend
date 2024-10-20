from rest_framework import serializers
from .models import *

# SERIALIZERS FOR ALL MODELS USE TO CONVERT COMPLEX DATA TO JSON
class CommodityDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommodityDetails
        fields = '__all__'

class MarketStatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketStates
        fields = '__all__'
class MarketDistrictsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketDistricts
        fields = '__all__'
class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketDetails
        fields = '__all__'
class PriceDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceDetails
        fields = '__all__'
class Top6MarketPricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Top6MarketPrices
        fields = '__all__'
class CommodityForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommodityForecast
        fields = '__all__'
class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity
        fields = '__all__'