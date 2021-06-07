from django.contrib import admin
from .models import Bundle, BundleItem


class BundleItemInline(admin.TabularInline):
    model = BundleItem


class BundleAdmin(admin.ModelAdmin):
    model = Bundle

    inlines = (BundleItemInline,)


admin.site.register(Bundle, BundleAdmin)