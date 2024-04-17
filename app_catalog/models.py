from django.db import models


class CafeBranch(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'branches'
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'

    def __str__(self):
        return f'Филиал: {self.name}'


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название категории')
    image = models.ImageField(upload_to='category_images', blank=True, null=True, verbose_name='Изображение')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    branch = models.ForeignKey(CafeBranch, on_delete=models.SET_NULL, blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        db_table = 'categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'Категория: {self.name}'


class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)

    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='media/item_images', blank=True, null=True, verbose_name='Изображение')

    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True, verbose_name='URL')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    def __str__(self):
        return f'Категория: {self.category.name} | Товар: {self.name}'

    class Meta:
        db_table = 'items'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class PizzaSizes(models.Model):
    size = models.PositiveSmallIntegerField(verbose_name='Размер в см.', blank=True, null=True)
    slug = models.SlugField(max_length=3, unique=True, blank=True, null=True, verbose_name='URL')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        db_table = 'pizza_sizes'
        verbose_name = 'Размер пиццы'
        verbose_name_plural = 'Размеры пиццы'

    def __str__(self):
        return f'Размер: {self.size} см.'


class ItemParams(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, null=True)
    count = models.PositiveSmallIntegerField(verbose_name='Количество в шт.', blank=True, null=True)
    size = models.ForeignKey(PizzaSizes, on_delete=models.SET_NULL, blank=True, null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Вес в гр.', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена в руб.', blank=False, null=False)

    class Meta:
        db_table = 'item_params'
        verbose_name = 'Параметры товара'
        verbose_name_plural = 'Параметры товара'

    def __str__(self):
        return f'Параметры для: {self.item.name}'


class PizzaBoard(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название борта')
    price25 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена для 25 см', blank=True, null=True)
    price32 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена для 32 см', blank=True, null=True)
    price43 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена для 43 см', blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True, verbose_name='URL')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        db_table = 'pizza_boards'
        verbose_name = 'Борт для пиццы'
        verbose_name_plural = 'Борт для пиццы'

    def __str__(self):
        return f'Борт для пиццы: {self.name}'
