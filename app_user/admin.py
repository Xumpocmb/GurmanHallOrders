from django.contrib import admin
from app_user.models import User, CartItem


@admin.register(User)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    search_fields = ['user']
