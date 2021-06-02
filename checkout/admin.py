from django.contrib import admin
from .models import Order, OrderItem, Address


class OrderItemAdminInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('item_total',)


class OrderAdmin(admin.ModelAdmin):

    inlines = (OrderItemAdminInline,)

    readonly_fields = ('order_id', 'date', 'delivery_surcharge',
                       'items_total', 'grand_total')

    fields = ('order_id', 'date', 'cust_name', 'cust_email',
              'cust_phone', 'address', 'items_total',
              'delivery_surcharge', 'grand_total')

    list_display = ('order_id', 'date', 'address', 'cust_name', 'cust_email',
                    'grand_total')

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Address)

