from django.contrib import admin
from .models import *


class ItemInline(admin.TabularInline):
    model = ItemOrder


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'f_name', 'l_name', 'address', 'create', 'paid', 'discount',
                    'get_price', 'code']
    inlines = [ItemInline]


class ItemOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'quantity', 'price', 'size']


class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'start', 'end', 'discount', 'active']


admin.site.register(Order, OrderAdmin)
admin.site.register(ItemOrder, ItemOrderAdmin)
admin.site.register(Coupon, CouponAdmin)
