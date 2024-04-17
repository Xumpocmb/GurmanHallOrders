# Generated by Django 5.0.4 on 2024-04-14 18:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_catalog', '0009_pizzaboard_is_active'),
        ('app_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Количество')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Создан')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_catalog.item', verbose_name='Товар')),
                ('item_params', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_catalog.itemparams', verbose_name='Параметры')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Товар в корзине',
                'verbose_name_plural': 'Товары в корзине',
                'db_table': 'cart_items',
            },
        ),
    ]