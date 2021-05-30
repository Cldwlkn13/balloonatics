from django.contrib import admin
from .models import Product, Category, Material, Sub_Category, Size, Color


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'category',
        'sub_category',
        'material',
        'name',
        'price'
    )


admin.site.register(Category)
admin.site.register(Material)
admin.site.register(Sub_Category)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Product, ProductAdmin)
