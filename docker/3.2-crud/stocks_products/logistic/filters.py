from django.db.models import Q
from django_filters import rest_framework as filters

from .models import Stock


class StockFilter(filters.FilterSet):
    products = filters.CharFilter(method='stock_filter',
                                  lookup_expr='icontains')

    class Meta:
        model = Stock
        fields = ['products']

    def stock_filter(self, queryset, name, value):
        if value.isdigit():
            return Stock.objects.filter(Q(products__id=value))
        else:
            return Stock.objects.filter(Q(products__title__icontains=value) | Q(products__description__icontains=value))

        # return queryset.filter(Q(ip_addr__icontains=value) | Q(virtual_ip__icontains=value))
