"""__author__ = 叶小永"""
from rest_framework import serializers

from carts.models import CartModel
from goods.serializers import GoodsSerializer


class CartSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = CartModel
        fields = '__all__'

    def to_representation(self, instance):
        # 被调用，self.get_serializer(queryset, many=True)
        # 将对象转换成序列化的结果
        data = super().to_representation(instance)
        data['c_goods'] = data['goods']
        del data['goods']
        data['c_goods_num'] = data['c_num']
        del data['c_num']
        data['c_is_select'] = data['is_select']
        del data['is_select']
        return data

