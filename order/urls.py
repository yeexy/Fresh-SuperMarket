"""__author__ = 叶小永"""
from rest_framework.routers import SimpleRouter

from order.views import OrderView

router = SimpleRouter()
router.register('orders', OrderView)

urlpatterns = [

]

urlpatterns += router.urls
