from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm
from django.shortcuts import get_object_or_404, redirect
from app_catalog.models import Item, ItemParams, PizzaSauce, Topping, PizzaBoard, PizzaAddons
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


@login_required(login_url='app_user:login')
def add_to_cart_view(request):
    user = request.user

    item_id = request.POST.get('item_id')
    param_id = request.POST.get('item-params')
    pizza_sauce = PizzaSauce.objects.filter(pk=request.POST.get('pizza_sauce')).first() if request.POST.get(
        'pizza_sauce') else None
    pizza_board = PizzaBoard.objects.filter(pk=request.POST.get('pizza_board')).first() if request.POST.get(
        'pizza_board') else None
    topping = Topping.objects.filter(pk=request.POST.get('souse-option')).first() if request.POST.get(
        'souse-option') else None
    addons_ids = request.POST.getlist('addons') if request.POST.getlist('addons') else None
    if addons_ids is not None:
        addons_ids = [int(addon) for addon in addons_ids]

    addons = PizzaAddons.objects.filter(pk__in=addons_ids) if addons_ids else None

    item = get_object_or_404(Item, pk=item_id)
    item_params = get_object_or_404(ItemParams, pk=param_id)

    if item_params.size:
        size = item_params.size
    elif item_params.count:
        size = item_params.count
    else:
        size = item_params.weight

    # Проверка наличия уже добавленного продукта в корзине
    existing_cart_item = CartItem.objects.filter(
        user=user,
        item=item,
        item_params=item_params,
        sauce_base=pizza_sauce,
        topping=topping,
        pizza_board=pizza_board
    )

    if addons_ids is not None:
        existing_cart_item = existing_cart_item.filter(addons__in=addons)

    existing_cart_item = existing_cart_item.first()

    if existing_cart_item:
        existing_cart_item.quantity += 1
        existing_cart_item.save()
        messages.success(request, f'{item.name} добавлен в корзину', extra_tags='success')
    else:
        cart_item = CartItem.objects.create(user=user, item=item, item_params=item_params, quantity=1,
                                            sauce_base=pizza_sauce, pizza_board=pizza_board, topping=topping)
        cart_item.addons.set(addons) if addons else None
        messages.success(request, f'{item.name} добавлен в корзину', extra_tags='success')
    return redirect('app_catalog:catalog')


@login_required(login_url='app_user:login')
def remove_from_cart_view(request, cart_id):
    cart_item = CartItem.objects.filter(id=cart_id).first()
    if cart_item:
        cart_item.delete()
        messages.success(request, 'Товар удален из корзины.', extra_tags='info')
    return redirect('app_user:cart')


@login_required(login_url='app_user:login')
def cart_view(request):
    context = {
        'title': 'Корзина',
    }
    return render(request, 'app_user/cart.html', context=context)
