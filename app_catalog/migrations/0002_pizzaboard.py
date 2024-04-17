# Generated by Django 5.0.4 on 2024-04-14 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PizzaBoard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название борта')),
                ('price25', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Цена для 25 см')),
                ('price32', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Цена для 32 см')),
                ('price43', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Цена для 43 см')),
                ('slug', models.SlugField(blank=True, max_length=100, null=True, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Борт для пиццы',
                'verbose_name_plural': 'Борт для пиццы',
                'db_table': 'pizza_boards',
            },
        ),
    ]
