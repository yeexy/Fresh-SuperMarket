"""__author__ = 叶小永"""
from rest_framework import serializers

from goods.models import MainShow, MainNav, MainWheel, FoodType, Goods


class ShowsSerializer(serializers.ModelSerializer):

    class Meta:
        model = MainShow
        fields = '__all__'


class NavSerializer(serializers.ModelSerializer):

    class Meta:
        model = MainNav
        fields = '__all__'


class WheelSerializer(serializers.ModelSerializer):

    class Meta:
        model = MainWheel
        fields = '__all__'


class FoodTypeSerializer(serializers.ModelSerializer):
    # 序列化商品类型
    class Meta:
        model = FoodType
        fields = '__all__'


class GoodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goods
        fields = '__all__'
