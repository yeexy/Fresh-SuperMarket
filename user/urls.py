"""__author__ = 叶小永"""
from rest_framework.routers import SimpleRouter

from user.views import UserView

# 获取路由对象
router = SimpleRouter()
# 注册资源，/api/user/auth/  /api/user/auth/[id]/
router.register('auth', UserView)

urlpatterns = [

]

# 添加路由地址到urlpatterns
urlpatterns += router.urls

