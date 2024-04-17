from django.urls import path
from app_order.views import order_create, orders, order_detail, change_order_status, download_pdf

app_name = 'app_order'

urlpatterns = [
    path('orders/', orders, name='orders'),
    path('order/<int:pk>/', order_detail, name='order_detail'),
    path('create/', order_create, name='order_create'),
    path('change_status/<int:pk>/<int:status>/', change_order_status, name='change_order_status'),
    path('download_pdf/<int:pk>/', download_pdf, name='download_pdf'),
]
