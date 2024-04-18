from django.shortcuts import render
from app_catalog.models import Item, Category, PizzaSauce, PizzaBoard


def catalog(request):
    context = {
        'title': 'Каталог',
        'categories': Category.objects.all(),
    }
    return render(request, 'app_catalog/catalog.html', context=context)


def category_detail(request, slug):
    category = Category.objects.filter(slug=slug).first()
    context = {
        'title': 'Категория',
        'category': category,
        'items': Item.objects.filter(category__slug=slug),
    }
    if slug == 'picca':
        context['sauces'] = PizzaSauce.objects.all()
        context['pizza_board'] = PizzaBoard.objects.all()
    return render(request, 'app_catalog/catalog.html', context=context)
