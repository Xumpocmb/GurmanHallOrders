# Generated by Django 5.0.4 on 2024-04-18 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_order', '0004_order_branch_alter_order_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='free_delivery',
            field=models.BooleanField(default=False),
        ),
    ]
