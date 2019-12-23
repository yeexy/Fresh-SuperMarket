"""__author__ = 叶小永"""
from django.urls import path
from rest_framework.routers import SimpleRouter

from goods.views import home, FoodTypeView, MarketView
# 获取路由对象
router = SimpleRouter()
# 注册一个资源
router.register('foodtype', FoodTypeView)

router.register('market', MarketView)

urlpatterns = [
    path('home/', home),
]

urlpatterns += router.urls
