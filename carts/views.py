from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework import mixins, viewsets

from carts.models import CartModel
from carts.serializers import CartSerializer
from utils.auth import UserLoginAuth


class CartView(viewsets.GenericViewSet,
               mixins.ListModelMixin,
               mixins.UpdateModelMixin):

    queryset = CartModel.objects.all()
    serializer_class = CartSerializer
    # 用户认证类，验证用户是否登录
    authentication_classes = (UserLoginAuth,)

    @action(detail=False, methods=['POST'])
    def add_cart(self, request):
        # 获取当前用户登录信息和商品信息
        # 1.通过前端传递的token获取用户信息
        # 2.如果找不到用户信息，说明用户没有登录
        # 3.如果找得到用户信息，说明登录了

        # 添加商品信息
        goodsid = request.data['goodsid']
        cart = CartModel.objects.filter(goods_id=goodsid, user=request.user).first()
        if cart:
            cart.c_num += 1
            cart.save()
        else:
            CartModel.objects.create(goods_id=goodsid, user=request.user)
        res = {'msg': '添加购物车成功'}
        return Response(res)

    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = self.get_queryset().filter(user=user)
        # 购物车总价格
        total_price = 0
        if queryset.filter(is_select=True).exists():
            for item in queryset.filter(is_select=True):
                total_price += item.goods.price * item.c_num
        # 全选按钮，默认不勾选
        all_select = False if CartModel.objects.filter(user=user, is_select=False) or \
                              (not CartModel.objects.all()) else True

        res = {
            'carts': self.get_serializer(queryset, many=True).data,
            'total_price': total_price,  # 总价格
            'all_select': all_select  # 全选按钮
        }
        return Response(res)

    def update(self, request, *args, **kwargs):
        # 修改当前商品的选择状态
        # 如果当前商品的is_select为1，修改为0
        cart = self.get_object()
        # cart.is_select = False if cart.is_select else True
        cart.is_select = not cart.is_select
        cart.save()
        res = {'msg': '操作成功'}
        return Response(res)

    @action(detail=False, methods=['POST'])
    def sub_cart(self, request):
        # 减少商品
        goodsid = request.data['goodsid']
        cart = CartModel.objects.filter(goods_id=goodsid, user=request.user).first()
        if cart.c_num > 1:
            cart.c_num -= 1
            cart.save()
        else:
            cart.delete()
        res = {'msg': '减少商品数量成功'}
        return Response(res)

    @action(detail=False, methods=['PATCH'])
    def change_select(self, request):
        # 全选
        user = request.user
        user_cart = CartModel.objects.filter(user=user, is_select=False)
        if user_cart:
            CartModel.objects.filter(user=user).update(is_select=True)
        else:
            CartModel.objects.filter(user=user).update(is_select=False)
        res = {'msg': '操作成功'}
        return Response(res)

