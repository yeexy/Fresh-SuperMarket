from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import mixins, viewsets

from goods.filters import GoodsFilter
from goods.models import MainWheel, MainNav, MainShow, FoodType, Goods

from goods.serializers import GoodsSerializer, WheelSerializer, \
    NavSerializer, FoodTypeSerializer, ShowsSerializer


@api_view(http_method_names=['GET'])
def home(request):

    wheels = MainWheel.objects.all()
    navs = MainNav.objects.all()
    shows = MainShow.objects.all()
    res = {
        # 序列化所有值，需要加一个参数many=True
        'main_wheels': WheelSerializer(wheels, many=True).data,
        'main_navs': NavSerializer(navs, many=True).data,
        'main_shows': ShowsSerializer(shows, many=True).data
    }
    return Response(res)


class FoodTypeView(viewsets.GenericViewSet,
                   mixins.ListModelMixin):
    # 定义查询集
    queryset = FoodType.objects.all()
    # 定义序列化类
    serializer_class = FoodTypeSerializer


class MarketView(viewsets.GenericViewSet,
                 mixins.ListModelMixin):

    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    # 添加过滤类
    filter_class = GoodsFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        """
        # 获取子分类id，不为0进行再次过滤
        childcid = request.GET.get('childcid')
        if childcid != '0':
            queryset = queryset.filter(childcid=childcid)

        # 获取排序规则信息，按不同的信息进行排序
        order_rule = request.GET.get('order_rule')
        if order_rule == '1':
            queryset = queryset.order_by('price')
        elif order_rule == '2':
            queryset = queryset.order_by('-price')
        elif order_rule == '3':
            queryset = queryset.order_by('productnum')
        else:
            queryset = queryset.order_by('-productnum')
        """

        serializer = self.get_serializer(queryset, many=True)

        # 解析分类信息
        typeid = request.GET.get('typeid')
        foodtype = FoodType.objects.filter(typeid=typeid).first()
        foodtype_list = foodtype.childtypenames.split('#')
        foodtype_data = []
        for item in foodtype_list:
            foodtype_dict = {}
            item_list = item.split(':')
            foodtype_dict['child_value'] = item_list[-1]
            foodtype_dict['child_name'] = item_list[0]
            foodtype_data.append(foodtype_dict)

        # 排序规则
        order_rule_data = [
            {'order_value': '1', 'order_name': '价格升序'},
            {'order_value': '2', 'order_name': '价格降序'},
            {'order_value': '3', 'order_name': '销量升序'},
            {'order_value': '4', 'order_name': '销量降序'},
        ]

        # 返回给前端的数据
        res = {
            'goods_list': serializer.data,
            'order_rule_list': order_rule_data,
            'foodtype_childname_list': foodtype_data
        }
        return Response(res)



