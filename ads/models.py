from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=150)
    lat = models.CharField(max_length=250)
    lng = models.CharField(max_length=250)

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'


class User(models.Model):
    ROLES = [
        ('member', 'Пользователь'),
        ('admin', 'Администратор'),
        ('moderator', 'Модератор'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=100, choices=ROLES, default='member')
    age = models.PositiveIntegerField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Ad(models.Model):
    name = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_ad')
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=300, null=True)
    is_published = models.BooleanField(default=True)
    image = models.ImageField(upload_to='logos/', null=True)
    category = models.ManyToManyField(Category)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
