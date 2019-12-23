import uuid

from django.core.cache import cache
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from order.models import OrderModel
from user.models import UserModel
from user.serializers import UserSerializer, \
    UserRegisterSerializer, UserLoginSerializer
from utils.errors import ParamsException


class UserView(viewsets.GenericViewSet,
               mixins.ListModelMixin,):
    # 定义查询集
    queryset = UserModel.objects.all()
    # 定义序列化类
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        token = request.query_params.get('token')
        user_id = cache.get(token)
        user = UserModel.objects.filter(pk=user_id).first()

        order_not_pay = OrderModel.objects.filter(user_id=user_id, o_status=0)
        order_not_send = OrderModel.objects.filter(user_id=user_id, o_status=2)

        res = {
            'user_info': self.get_serializer(user).data,
            'orders_not_pay_num': order_not_pay.count(),
            'orders_not_send_num': order_not_send.count()
        }
        return Response(res)

    # @list_route，将函数名作为接口地址的一部分
    @action(detail=False, serializer_class=UserRegisterSerializer,
            methods=['POST'])
    def register(self, request):
        # 触发该函数，接口地址为：/api/user/auth/register/
        # 1.校验数据
        serializer = self.get_serializer(data=request.data)
        result = serializer.is_valid(raise_exception=False)
        # 2.判断校验结果
        if not result:
            errors = serializer.errors
            res = {
                'code': 1001,
                'msg': '字段校验失败',
                'data': errors
            }
            raise ParamsException(res)
        user = serializer.save()
        res = {'user_id': user.id}
        return Response(res)

    @action(detail=False, serializer_class=UserLoginSerializer,
            methods=['POST'])
    def login(self, request):

        serializer = self.get_serializer(data=request.data)
        result = serializer.is_valid(raise_exception=False)
        if not result:
            errors = serializer.errors
            res = {
                'code': 1005,
                'msg': '字段校验失败',
                'data': errors
            }
            raise ParamsException(res)
        # # 生成一个随机token
        # token = uuid.uuid4().hex
        # if not request.session.get('axf_token'):
        #     # 保存token到redis
        #     request.session['username'] = request.POST.get('u_username')
        #     request.session['password'] = request.POST.get('u_password')
        #     request.session['axf_token'] = token
        # # 返回一个token
        # res = {'token': token}

        token = serializer.login_user(serializer.data)
        res = {'token': token}
        return Response(res)

