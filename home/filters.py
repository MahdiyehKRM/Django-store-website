import django_filters
from django import forms
from .models import *


class ProductFilter(django_filters.FilterSet):
    Choice_1 = {
        ('گران ترین', 'گران ترین'),
        ('ارزان ترین', 'ارزان ترین'),
    }

    Choice_2 = {
        ('old', 'قدیم'),
        ('جدیدترین', 'جدیدترین'),
    }

    Choice_3 = {
        ('s', 'کم تخفیف'),
        ('پر تخفیف ترین', 'پر تخفیف ترین'),
    }

    Choice_4 = {
        ('s', 'کم فروش'),
        ('پر فروش ترین', 'پر فروش ترین'),
    }
    Choice_6 = {
        ('f', 'کم محبوب'),
        ('پربازدیدترین', 'پربازدیدترین'),
    }

    class Meta:
        model = Product
        fields = ['available']

    price_1 = django_filters.NumberFilter(field_name='total_price', lookup_expr='gte')
    price_2 = django_filters.NumberFilter(field_name='total_price', lookup_expr='lte')

    size = django_filters.ModelMultipleChoiceFilter(queryset=Size.objects.all(), widget=forms.CheckboxSelectMultiple)
    color = django_filters.ModelMultipleChoiceFilter(queryset=Color.objects.all(), widget=forms.CheckboxSelectMultiple)
    brand = django_filters.ModelMultipleChoiceFilter(queryset=Brand.objects.all(), widget=forms.CheckboxSelectMultiple)
    category = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.filter(sub_cat=False), widget=forms.CheckboxSelectMultiple)
    price = django_filters.ChoiceFilter(choices=Choice_1, method='price_filter')
    create = django_filters.ChoiceFilter(choices=Choice_2, method='create_filter')
    discount = django_filters.ChoiceFilter(choices=Choice_3, method='discount_filter')

    def price_filter(self, queryset, name, value):
        data = 'total_price' if value == 'ارزان ترین' else '-total_price'
        return queryset.order_by(data)

    def create_filter(self, queryset, name, value):
        data = 'create' if value == 'old' else '-create'
        return queryset.order_by(data)

    def discount_filter(self, queryset, name, value):
        data = 'discount' if value == 's' else '-discount'
        return queryset.order_by(data)




