from django.shortcuts import render
from app_catalog.models import Item, Category, PizzaSauce, PizzaBoard, PizzaAddons, Topping


def catalog(request):
    context = {
        'title': 'Каталог',
        'categories': Category.objects.filter(is_active=True),
    }
    return render(request, 'app_catalog/catalog.html', context=context)


def category_detail(request, slug):
    category = Category.objects.filter(slug=slug, is_active=True).first()
    context = {
        'title': category.name,
        'category': category,
        'items': Item.objects.filter(category__slug=slug, is_active=True),
    }
    if category.slug == 'picca':
        context['pizza_addons'] = PizzaAddons.objects.filter(is_active=True)
        context['pizza_sauces'] = PizzaSauce.objects.filter(is_active=True)
        context['pizza_boards'] = PizzaBoard.objects.filter(is_active=True)
    if category.slug == 'zapechennye-rolly':
        context['toppings'] = Topping.objects.filter(is_active=True)
    return render(request, 'app_catalog/catalog.html', context=context)
