from django.shortcuts import render
from app_order.models import Order
from app_user.models import User, CartItem
from django.http import HttpResponseRedirect
from django.contrib import messages
from app_order.forms import OrderForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.http import HttpResponse
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from app_catalog.models import CafeBranch


def orders(request):
    context = {
        'title': 'Заказы',
        'orders': Order.objects.filter(customer__username=request.user.username),
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


def generate_pdf(order):

    pdfmetrics.registerFont(TTFont('Arial', 'static/fonts/Arial.ttf', 'UTF-8'))

    # Создаем буфер для PDF файла
    buffer = BytesIO()

    # Создаем PDF документ
    doc = SimpleDocTemplate(buffer, pagesize=A4, title=f'Детали заказа {order.display_id()}',)

    # Получаем стили для абзацев
    styles = getSampleStyleSheet()
    styles['Normal'].fontName = 'Arial'
    styles['Heading1'].fontName = 'Arial'
    styles['Heading3'].fontName = 'Arial'
    normal_style = styles['Normal']
    heading_style1 = styles['Heading1']
    heading_style3 = styles['Heading3']

    # Создаем список для содержимого PDF
    content = []

    # Заголовок
    content.append(Paragraph(f'Детали заказа {order.display_id()}', heading_style3))
    content.append(Paragraph(f'{order.branch.name}', heading_style1))
    content.append(Paragraph(f'{order.branch.phone1}', heading_style3))
    content.append(Paragraph(f'{order.branch.phone2}', heading_style3))

    # Строка с датой и временем
    date_string = order.created_at.strftime('%d-%m-%Y %H:%M')
    content.append(Paragraph(f'Дата: {date_string}', normal_style))

    # Данные для заказа
    data = [
        f'Заказчик: {order.first_name}',
        f'Адрес: {order.address}',
        f'Телефон: {order.phone}',
        f'Description: {order.description}',
        f'Способ доставки: {order.delivery_method}',
        f'Способ оплаты: {order.get_payment_method_display()}',
    ]

    # Создаем абзацы и добавляем их в список содержимого
    for item in data:
        paragraph = Paragraph(item, normal_style)
        content.append(paragraph)

    if order.delivery_method == 'Курьер':
        if order.free_delivery:
            content.append(Paragraph('Доставка: Бесплатная доставка', normal_style))

    # Корзина
    content.append(Paragraph('Товар(ы):', heading_style1))

    for basket in order.basket_history['baskets']:
        product_name = basket['product_name']
        quantity = basket['quantity']
        price = basket['price']
        basket_sum = basket['sum']
        sauce = basket['sauce']
        topping = basket['topping']
        pizza_board = basket['pizza_board']

        content.append(Paragraph(f'{product_name}: {quantity}', heading_style3))
        params = basket['params']
        if params['size']:
            content.append(Paragraph(f'Размер: {params['size']}', normal_style))
        if params['count']:
            content.append(Paragraph(f'Шт.: {params['count']}', normal_style))
        if params['weight']:
            content.append(Paragraph(f'Гр.: {params['weight']}', normal_style))
        if sauce:
            content.append(Paragraph(f'{sauce}', normal_style))
        if topping:
            content.append(Paragraph(f'{topping}', normal_style))
        if pizza_board:
            content.append(Paragraph(f'{pizza_board}', normal_style))
        content.append(Paragraph(f'Цена: {price}', normal_style))
        content.append(Paragraph(f'Сумма товара: {basket_sum}', normal_style))

    # Общая сумма
    content.append(Paragraph(f'Общая сумма заказа: {order.basket_history['total_sum']}', heading_style1))

    # Добавляем содержимое в PDF документ
    doc.build(content)

    # Получаем содержимое буфера
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


def download_pdf(request, pk):
    order = Order.objects.get(pk=pk)
    pdf_content = generate_pdf(order)
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{order.display_id()}.pdf"'
    return response
