# Generated by Django 5.0.4 on 2024-04-14 12:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_catalog', '0006_pizzasizes_is_active_pizzasizes_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemparams',
            name='size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_catalog.pizzasizes'),
        ),
    ]
