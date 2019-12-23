"""__author__ = 叶小永"""
from order.models import OrderModel

import django_filters


class OrderFilter(django_filters.rest_framework.FilterSet):
    # o_status为all、not_pay、not_send
    o_status = django_filters.CharFilter(method='filter_status')

    class Meta:
        model = OrderModel
        fields = ['o_status']

    def filter_status(self, queryset, name, value):
        if value == 'all':
            return queryset
        elif value == 'not_pay':
            return queryset.filter(o_status=0)
        else:
            return queryset.filter(o_status=2)



