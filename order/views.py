import uuid

from rest_framework import mixins, viewsets
from rest_framework.response import Response

from carts.models import CartModel
from goods.models import Goods
from order.filters import OrderFilter
from order.models import OrderModel, OrderGoodsModel
from order.serializers import OrderSerializer
from utils.auth import UserLoginAuth


class OrderView(viewsets.GenericViewSet,
                mixins.ListModelMixin,
                mixins.CreateModelMixin):

    # 定义查询集
    queryset = OrderModel.objects.all()
    # 定义序列化类
    serializer_class = OrderSerializer
    # 用户认证类
    authentication_classes = (UserLoginAuth,)
    # 过滤类
    filter_class = OrderFilter

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # 下单功能
        # 将购物车中已选择的商品加入到订单中
        # 1.选择已勾选的商品
        # 2.创建订单，OrderModel
        # 3.创建订单详情表，OrderGoodsModel
        # 4.把购物车中刚下单的商品删除
        user = request.user
        cart = CartModel.objects.filter(user=user, is_select=True)
        if cart.exists():
            # 创建订单表
            o_num = uuid.uuid4().hex
            order = OrderModel.objects.create(user=user, o_num=o_num)
            for item in cart:
                # 创建订单详情表
                goods = Goods.objects.get(pk=item.goods_id)
                OrderGoodsModel.objects.create(goods=goods, order=order, goods_num=item.c_num)
            # 删除购物车中已下单的商品
            cart.delete()
            res = {'msg': '下单成功'}
        else:
            res = {'code': 1010, 'msg': '你未选择任何商品'}
        return Response(res)


