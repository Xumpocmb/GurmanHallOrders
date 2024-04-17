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
    normal_style = styles['Normal']
    heading_style = styles['Heading1']

    # Создаем список для содержимого PDF
    content = []

    # Заголовок
    content.append(Paragraph(f'Детали заказа {order.display_id()}', heading_style))

    # Данные для заказа
    data = [
        f'First Name: {order.first_name}',
        f'Last Name: {order.last_name}',
        f'Email: {order.email}',
        f'Address: {order.address}',
        f'Phone: {order.phone}',
        f'Description: {order.description}',
        f'Delivery Method: {order.delivery_method}',
        f'Payment Method: {order.get_payment_method_display()}',
    ]

    # Создаем абзацы и добавляем их в список содержимого
    for item in data:
        paragraph = Paragraph(item, normal_style)
        content.append(paragraph)

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
