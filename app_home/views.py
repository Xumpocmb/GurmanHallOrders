from django.shortcuts import render


def index(request):
    context = {
        'title': 'Главная',
    }
    return render(request, 'app_home/index.html', context=context)
