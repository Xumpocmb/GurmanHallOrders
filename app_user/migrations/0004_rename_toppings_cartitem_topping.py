# Generated by Django 5.0.4 on 2024-04-18 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0003_cartitem_sauce_base_cartitem_toppings'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='toppings',
            new_name='topping',
        ),
    ]
