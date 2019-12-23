"""__author__ = 叶小永"""
from rest_framework import serializers

from goods.serializers import GoodsSerializer
from order.models import OrderModel


class OrderSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # 该订单所对应的订单商品详情内容
        order_goods = instance.ordergoodsmodel_set.all()
        goods_info = []
        total_price = 0
        # 循环获取商品信息
        for o_g in order_goods:
            result = {
                'o_goods': GoodsSerializer(o_g.goods).data
            }
            goods_info.append(result)
            # 每个订单的总价
            total_price += o_g.goods_num * o_g.goods.price

        data['order_goods_info'] = goods_info
        data['o_price'] = total_price
        # data['o_status']
        return data

    class Meta:
        model = OrderModel
        fields = '__all__'


