# Generated by Django 5.0.4 on 2024-04-18 13:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_catalog', '0012_topping_alter_pizzasauce_options'),
        ('app_user', '0004_rename_toppings_cartitem_topping'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='pizza_board',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_catalog.pizzaboard', verbose_name='Борт для пиццы'),
        ),
    ]
