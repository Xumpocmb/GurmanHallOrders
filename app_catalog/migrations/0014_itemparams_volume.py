# Generated by Django 5.0.4 on 2024-05-27 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_catalog', '0013_pizzaaddons_remove_pizzaboard_price25_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemparams',
            name='volume',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Объем в л.'),
        ),
    ]