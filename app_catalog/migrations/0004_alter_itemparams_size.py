# Generated by Django 5.0.4 on 2024-04-14 12:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_catalog', '0003_pizzasizes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemparams',
            name='size',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_catalog.pizzasizes'),
        ),
    ]
