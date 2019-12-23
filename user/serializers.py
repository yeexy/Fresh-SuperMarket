"""__author__ = 叶小永"""
import uuid

from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from rest_framework import serializers

from user.models import UserModel
from utils.errors import ParamsException


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        # 定义需要序列化的模型
        model = UserModel
        # 定义需要序列化的字段
        fields = ['username']


class UserRegisterSerializer(serializers.Serializer):
    u_username = serializers.CharField(required=True, max_length=32,
                                       min_length=5,
                                       error_messages={
                                           'required': '用户名不能为空',
                                           'max_length': '用户名不能超过32个字符',
                                           'min_length': '用户名不能小于5个字符'
                                       })
    u_password = serializers.CharField(required=True, max_length=16,
                                       min_length=6,
                                       error_messages={
                                           'required': '密码不能为空',
                                           'max_length': '密码不能超过16个字符',
                                           'min_length': '密码不能小于6个字符'
                                       })
    u_password2 = serializers.CharField(required=True, max_length=16,
                                        min_length=6,
                                        error_messages={
                                            'required': '确认密码不能为空',
                                            'max_length': '确认密码不能超过16个字符',
                                            'min_length': '确认密码不能小于6个字符'
                                        })
    u_email = serializers.EmailField(required=True, max_length=64,
                                     min_length=4,
                                     error_messages={
                                         'required': '邮箱不能为空',
                                         'max_length': '邮箱不能超过64个字符',
                                         'min_length': '邮箱不能小于4个字符'
                                     })

    def validate(self, attrs):
        # 校验用户名是否存在
        u_username = attrs['u_username']
        if UserModel.objects.filter(username=u_username).exists():
            res = {
                'code': 1002,
                'msg': '用户名已存在'
            }
            raise ParamsException(res)
        # 校验两次密码输入是否一致
        u_password = attrs['u_password']
        u_password2 = attrs['u_password2']
        if u_password != u_password2:
            res = {
                'code': 1003,
                'msg': '密码和确认密码不一致'
            }
            raise ParamsException(res)
        # 校验邮箱是否存在
        u_email = attrs['u_email']
        if UserModel.objects.filter(email=u_email).exists():
            res = {
                'code': 1004,
                'msg': '邮箱已注册'
            }
            raise ParamsException(res)
        return attrs

    def create(self, validated_data):
        # 重构保存方法
        username = validated_data['u_username']
        password = make_password(validated_data['u_password'])
        email = validated_data['u_email']
        user = UserModel.objects.create(username=username,
                                        password=password,
                                        email=email)
        return user

    class Meta:
        model = UserModel
        fields = '__all__'


class UserLoginSerializer(serializers.Serializer):
    u_username = serializers.CharField(required=True, max_length=32,
                                       min_length=5,
                                       error_messages={
                                           'required': '用户名不能为空',
                                           'max_length': '用户名不能超过32个字符',
                                           'min_length': '用户名不能小于5个字符'
                                       })
    u_password = serializers.CharField(required=True, max_length=16,
                                       min_length=6,
                                       error_messages={
                                           'required': '密码不能为空',
                                           'max_length': '密码不能超过16个字符',
                                           'min_length': '密码不能小于6个字符'
                                       })

    # 校验用户名和密码
    def validate(self, attrs):
        u_username = attrs['u_username']
        u_password = attrs['u_password']
        # 获取用户信息
        user = UserModel.objects.filter(username=u_username).first()
        if not user:
            res = {
                'code': 1006,
                'msg': '该用户不存在，请去注册'
            }
            raise ParamsException(res)
        if not check_password(u_password, user.password):
            res = {
                'code': 1007,
                'msg': '密码或用户名不正确'
            }
            raise ParamsException(res)
        return attrs

    def login_user(self, data):
        # 生成一个随机的登录标识符
        token = uuid.uuid4().hex
        user = UserModel.objects.filter(username=data['u_username']).first()
        # 使用redis进行存储，string类型
        cache.set(token, user.id, timeout=30000)
        return token

    class Meta:
        model = UserModel
        fields = '__all__'

