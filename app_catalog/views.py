from django.shortcuts import render
from app_catalog.models import Item, Category, PizzaSauce, PizzaBoard


def catalog(request):
    context = {
        'title': 'Каталог',
        'categories': Category.objects.filter(is_active=True),
    }
    return render(request, 'app_catalog/catalog.html', context=context)


def category_detail(request, slug):
    category = Category.objects.filter(slug=slug, is_active=True).first()
    context = {
        'title': 'Категория',
        'category': category,
        'items': Item.objects.filter(category__slug=slug, is_active=True),
    }
    if slug == 'picca':
        context['sauces'] = PizzaSauce.objects.filter(is_active=True)
        context['pizza_board'] = PizzaBoard.objects.filter(is_active=True)
    return render(request, 'app_catalog/catalog.html', context=context)
