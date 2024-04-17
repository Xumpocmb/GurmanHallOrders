from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm
from django.shortcuts import get_object_or_404, redirect
from app_catalog.models import Item, ItemParams
from app_user.models import CartItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def register_view(request):
    context = {
        'title': 'Регистрация',
        'form': UserRegistrationForm(),
    }
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('app_home:home')
        else:
            context['message_error'] = form.errors
    return render(request, 'app_user/register.html', context=context)


def login_view(request):
    context = {
        'title': 'Вход',
        'form': UserRegistrationForm(),
    }
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect('app_home:home')
        else:
            context['message_error'] = 'Неверное имя пользователя или пароль'
            return render(request, 'app_user/login.html', context=context)
    return render(request, 'app_user/login.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('app_home:home')


@login_required
def add_to_cart_view(request, item_id, param_id):
    item = get_object_or_404(Item, pk=item_id)
    item_params = get_object_or_404(ItemParams, pk=param_id)
    user = request.user

    existing_cart_item = CartItem.objects.filter(user=user, item=item, item_params=item_params).first()

    if existing_cart_item:
        existing_cart_item.quantity += 1
        existing_cart_item.save()
        messages.success(request, f'{item.name} добавлен в корзину', extra_tags='success')
    else:
        CartItem.objects.create(user=user, item=item, item_params=item_params, quantity=1)
        messages.success(request, f'{item.name} добавлен в корзину', extra_tags='success')
    return redirect('app_catalog:catalog')


@login_required
def remove_from_cart_view(request, cart_id):
    cart_item = CartItem.objects.filter(id=cart_id).first()
    if cart_item:
        cart_item.delete()
        messages.success(request, 'Товар удален из корзины.', extra_tags='info')
    return redirect('app_user:cart')


def cart_view(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    total_price = sum(item.sum() for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'title': 'Корзина',
    }
    return render(request, 'app_user/cart.html', context=context)
