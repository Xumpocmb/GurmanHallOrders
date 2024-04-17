from django.shortcuts import render
from app_catalog.models import Item, Category


def catalog(request):
    context = {
        'title': 'Каталог',
        'categories': Category.objects.all(),
    }
    return render(request, 'app_catalog/catalog.html', context=context)


def category_detail(request, slug):
    context = {
        'title': 'Категория',
        'category': Category.objects.get(slug=slug),
        'items': Item.objects.filter(category__slug=slug),
    }
    return render(request, 'app_catalog/catalog.html', context=context)
