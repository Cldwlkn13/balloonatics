from django.contrib import admin

from .models import Bundle, BundleItem, BundleCategory


class BundleItemInline(admin.TabularInline):
    model = BundleItem


class BundleAdmin(admin.ModelAdmin):
    inlines = (BundleItemInline,)


admin.site.register(BundleCategory)
admin.site.register(Bundle, BundleAdmin)
admin.site.register(BundleItem)
