from django.contrib import admin
from app_order.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', ]
    fields = ['id', 'status', 'created_at', 'updated_at', 'customer',
              ('first_name', 'last_name', 'email', 'address', 'phone',),
              'delivery_method', 'basket_history']
    list_filter = ['status']
    readonly_fields = ['id', 'created_at', 'updated_at', 'customer', 'basket_history']
