from django.contrib import admin
from .models import *
import admin_thumbnails


@admin_thumbnails.thumbnail('image')
class ImageInlines(admin.TabularInline):
    model = Images
    extra = 2


class ProductVariantInlines(admin.TabularInline):
    model = Variants
    extra = 2


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'sub_category')
    list_filter = ('name',)
    prepopulated_fields = {
        'slug': ('name',)
    }


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'create', 'update', 'amount', 'available', 'unit_price', 'discount', 'total_price']
    list_filter = ('available', 'status')
    list_editable = ('amount',)
    inlines = [ProductVariantInlines, ImageInlines]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Variants)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Brand)
admin.site.register(Comment)
admin.site.register(UserWishlist)
admin.site.register(Chart)

