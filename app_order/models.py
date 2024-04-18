from django.db import models

from app_user.models import User
from app_user.models import CartItem
from app_catalog.models import CafeBranch


class Order(models.Model):
    CREATED = 0
    CONFIRMED = 1
    PROCESSING = 2
    READY = 3
    ON_WAY = 4
    DELIVERED = 5
    CANCELLED = 6

    STATUSES = (
        (CREATED, 'Создан'),
        (CONFIRMED, 'Подтвержден'),
        (PROCESSING, 'В обработке'),
        (READY, 'Готов'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Выдан'),
        (CANCELLED, 'Отменен'),
    )

    PAYMENT_METHODS = (
        (1, 'Наличные'),
        (2, 'Банковская карта'),
    )

    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    basket_history = models.JSONField(default=dict)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    branch = models.ForeignKey(CafeBranch, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_method = models.CharField(max_length=255, null=False, blank=False)
    payment_method = models.SmallIntegerField(default=1, choices=PAYMENT_METHODS)
    free_delivery = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        formatted_date = self.created_at.strftime('%d-%m-%Y %H:%M')
        return f'Заказ № {self.id} | {formatted_date} | {self.customer} | {self.get_status_display()}'

    def display_id(self):
        return f'Order-#{self.id:06}'

    def fill_basket_history(self):
        carts = CartItem.objects.filter(user=self.customer)
        total_sum = float(carts.total_sum())
        basket_history = {
            'baskets': [basket.de_json() for basket in carts],
            'total_sum': total_sum
        }
        self.basket_history = basket_history

        if self.delivery_method == 'Курьер':
            if total_sum > 20:
                self.free_delivery = True
            else:
                self.free_delivery = False
        carts.delete()
        self.save()

