"""__author__ = 叶小永"""
from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication

from user.models import UserModel
from utils.errors import ParamsException


class UserLoginAuth(BaseAuthentication):
    # 判断用户是否登录
    def authenticate(self, request):
        token = request.data['token'] if request.data.get('token') else request.query_params.get('token')
        if not token:
            res = {
                'code': 1009,
                'msg': '您还未登录，请去登录'
            }
            raise ParamsException(res)
        user_id = cache.get(token)
        if not user_id:
            res = {
                'code': 1009,
                'msg': '登录信息已过期，请重新登录'
            }
            raise ParamsException(res)
        user = UserModel.objects.get(pk=user_id)
        return user, token



