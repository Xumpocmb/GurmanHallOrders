from django.db import models
from django.contrib.auth.models import AbstractUser
from app_catalog.models import Item, ItemParams
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    CHEF = 'Шеф'
    OPERATOR = 'Оператор'
    COURIER = 'Курьер'
    USER = 'Пользователь'

    ROLES = (
        (CHEF, 'Шеф'),
        (OPERATOR, 'Оператор'),
        (COURIER, 'Курьер'),
        (USER, 'Пользователь'),
    )

    role = models.CharField(max_length=20, choices=ROLES, default='user', verbose_name='Роль', null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации', null=True, blank=True)
    last_login = models.DateTimeField(auto_now=True, verbose_name='Последний вход', null=True, blank=True)
    is_archived = models.BooleanField(default=False, verbose_name='Архивирован', null=True, blank=True)

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']

    def __str__(self):
        return f'Пользователь: {self.username}'

    def display_id(self):
        return f'ID: {self.id:05}'


class CartQuerySet(models.QuerySet):
    def total_quantity(self):
        return sum(item.quantity for item in self)

    def total_sum(self):
        return sum(item.sum() for item in self)


class CartItem(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Пользователь', null=True, blank=True)
    item = models.ForeignKey(to=Item, on_delete=models.CASCADE, verbose_name='Товар', null=True, blank=True)
    item_params = models.ForeignKey(to=ItemParams, on_delete=models.CASCADE, verbose_name='Параметры', null=True, blank=True)
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество', null=True, blank=True)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан', null=True, blank=True)

    objects = CartQuerySet.as_manager()

    class Meta:
        db_table = 'cart_items'
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def __str__(self):
        return f'Корзина: {self.user.username} | Продукт: {self.item.name}'

    def sum(self):
        return self.item_params.price * self.quantity

    def de_json(self):
        items = {
            'product_name': self.item.name,
            'price': float(self.item_params.price),
            'sum': float(self.sum()),
            'quantity': self.quantity,
            'description': self.description or '',
            'params': {
                'size': float(self.item_params.size.size) if self.item_params.size else None,
                'count': float(self.item_params.count) if self.item_params.count else None,
                'weight': float(self.item_params.weight) if self.item_params.weight else None
            }
        }
        return items