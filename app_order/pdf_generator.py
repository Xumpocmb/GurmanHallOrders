from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from io import BytesIO

def register_fonts():
    pdfmetrics.registerFont(TTFont('Arial', 'static/fonts/Arial.ttf', 'UTF-8'))

def create_paragraphs(data, style):
    return [Paragraph(item, style) for item in data]

def add_order_details(order, content, normal_style, heading_style1, heading_style3):
    content.append(Paragraph(f'Детали заказа {order.display_id()}', heading_style3))
    content.append(Paragraph(f'{order.branch.name}', heading_style1))
    content.append(Paragraph(f'{order.branch.phone1}', heading_style3))
    content.append(Paragraph(f'{order.branch.phone2}', heading_style3))

    date_string = order.created_at.strftime('%d-%m-%Y %H:%M')
    content.append(Paragraph(f'Дата: {date_string}', normal_style))

    data = [
        f'Заказчик: {order.first_name}',
        f'Адрес: {order.address}',
        f'Телефон: {order.phone}',
        f'Описание: {order.description}',
        f'Способ доставки: {order.delivery_method}',
        f'Способ оплаты: {order.get_payment_method_display()}',
    ]

    content.extend(create_paragraphs(data, normal_style))

    if order.delivery_method == 'Курьер':
        if order.free_delivery == 0.0:
            content.append(Paragraph('Стоимость доставки: Бесплатная', normal_style))
        else:
            content.append(Paragraph(f'Стоимость доставки: {order.free_delivery} руб.', normal_style))

def add_basket_items(order, content, normal_style, heading_style3):
    content.append(Paragraph('Товар(ы):', heading_style3))

    for basket in order.basket_history['baskets']:
        product_name = basket['product_name']
        quantity = basket['quantity']
        basket_sum = basket['sum']
        sauce = basket['sauce']
        topping = basket['topping']
        pizza_board = basket['pizza_board']
        addons = basket['addons']

        content.append(Paragraph(f'{product_name}: {quantity}', heading_style3))
        params = basket['params']
        if params['size']:
            content.append(Paragraph(f'Размер: {params["size"]}', normal_style))
        if params['count']:
            content.append(Paragraph(f'Шт.: {params["count"]}', normal_style))
        if params['volume']:
            content.append(Paragraph(f'Л.: {params["volume"]}', normal_style))
        if params['weight']:
            content.append(Paragraph(f'Гр.: {params["weight"]}', normal_style))
        if sauce:
            content.append(Paragraph(f'Соус основа: {sauce}', normal_style))
        if topping:
            content.append(Paragraph(f'Шапочка: {topping}', normal_style))
        if pizza_board:
            pizza_board_name = pizza_board['name']
            pizza_board_price = pizza_board['price']
            content.append(Paragraph(f'Борт: {pizza_board_name} | Цена: {pizza_board_price}', normal_style))
        if addons:
            content.append(Paragraph('Добавки:', normal_style))
            for addon_name, addon_price in addons.items():
                content.append(Paragraph(f'- {addon_name}: {addon_price} руб.', normal_style))
        content.append(Paragraph(f'Сумма товара: {basket_sum}', normal_style))

    content.append(Paragraph(f'Общая сумма заказа: {order.basket_history["total_sum"]}', heading_style3))

def generate_pdf(order):
    register_fonts()

    # Создаем буфер для PDF файла
    buffer = BytesIO()

    # Создаем PDF документ
    doc = SimpleDocTemplate(buffer, pagesize=A4, title=f'Детали заказа {order.display_id()}')

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

    add_order_details(order, content, normal_style, heading_style1, heading_style3)
    add_basket_items(order, content, normal_style, heading_style3)

    # Добавляем содержимое в PDF документ
    doc.build(content)

    # Получаем содержимое буфера
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
