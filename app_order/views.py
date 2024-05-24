from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from app_catalog.models import CafeBranch
from app_order.forms import OrderForm
from app_order.models import Order
from app_user.models import User, CartItem
from .pdf_generator import generate_pdf


def orders_view(request):
    status_filter = request.GET.get('status')
    if status_filter is not None:
        orders = Order.objects.filter(customer__username=request.user.username, status=status_filter)
    else:
        orders = Order.objects.filter(customer__username=request.user.username)
    context = {
        'title': 'Заказы',
        'orders': orders,
        'order_statuses': Order.STATUSES  # ORDER_STATUSES,
    }
    return render(request, 'app_order/orders.html', context=context)


@login_required
def order_create(request):
    context = {
        'title': 'Оформление заказа',
        'branches': CafeBranch.objects.filter(is_active=True),
        'form': OrderForm(),
    }

    user_cart_items = CartItem.objects.filter(user=request.user)
    if not user_cart_items.exists():
        messages.error(request, 'Ваша корзина пуста. Добавьте товары перед оформлением заказа.', extra_tags='danger')
        return HttpResponseRedirect(reverse('app_catalog:catalog'))

    if request.method == 'POST':
        form = OrderForm(request.POST)
        form.instance.customer = User.objects.get(username=request.user.username)
        if form.is_valid():
            user_order = form.save()
            user_order.fill_basket_history()
            messages.success(request, 'Заказ оформлен', extra_tags='success')
            return HttpResponseRedirect(reverse('app_order:orders'))
        else:
            messages.error(request, 'Ошибка при оформлении заказа!', extra_tags='danger')
    return render(request, 'app_order/order_create.html', context=context)


@login_required
def order_detail(request, pk):
    context = {
        'title': 'Заказ',
        'order': Order.objects.get(pk=pk),
    }
    return render(request, 'app_order/order_detail.html', context=context)


@login_required
def change_order_status(request, pk, status):
    order = Order.objects.get(pk=pk)
    order.status = status
    order.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def download_pdf(request, pk):
    order = Order.objects.get(pk=pk)
    pdf_content = generate_pdf(order)
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{order.display_id()}.pdf"'
    return response
