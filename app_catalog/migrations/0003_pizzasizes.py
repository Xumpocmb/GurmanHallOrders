# Generated by Django 5.0.4 on 2024-04-14 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_catalog', '0002_pizzaboard'),
    ]

    operations = [
        migrations.CreateModel(
            name='PizzaSizes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Размер в см.')),
            ],
            options={
                'verbose_name': 'Размер пиццы',
                'verbose_name_plural': 'Размеры пиццы',
                'db_table': 'pizza_sizes',
            },
        ),
    ]
