from django.contrib import admin
from app_catalog.models import Category, Item, ItemParams, PizzaBoard, CafeBranch, PizzaSizes, PizzaSauce, Topping


@admin.register(CafeBranch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_active']


class ItemParamsInline(admin.TabularInline):
    model = ItemParams
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_active']
    list_editable = ['is_active']
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [ItemParamsInline]

    list_display = ['__str__', 'is_active']
    search_fields = ['name']
    list_filter = ['category', 'is_active']
    prepopulated_fields = {"slug": ("name",)}


@admin.register(PizzaBoard)
class PizzaBoardAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    prepopulated_fields = {"slug": ("name",)}


@admin.register(PizzaSizes)
class PizzaSizesAdmin(admin.ModelAdmin):
    list_display = ['size']
    prepopulated_fields = {"slug": ("size",)}


@admin.register(PizzaSauce)
class PizzaSauceAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {"slug": ("name",)}
