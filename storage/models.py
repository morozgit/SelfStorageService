from django.db import models
from django.contrib.auth.models import User
from django.db.models import Min


class Client(models.Model):
    user = models.OneToOneField(User,
                                verbose_name='Клиент',
                                on_delete=models.CASCADE,
                                primary_key=True,
                                related_name='client')
    address = models.TextField(verbose_name='Адрес клиента',
                               blank=True,
                               null=True)
    phonenumber = models.CharField(verbose_name='Номер телефона',
                                   max_length=50,
                                   null=True,
                                   blank=True)

    @property
    def user_email(self):
        return self.user.email

    @property
    def user_name(self):
        return self.user.first_name

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

    def __str__(self):
        return f'{self.user_name}: {self.address}, {self.phonenumber}'


class StorageQuerySet(models.QuerySet):
    def get_boxes(self):
        for storage in self:
            storage.count_of_free_boxes = storage.boxes.filter(is_occupied=False).count()
            storage.count_boxes = storage.boxes.count()
            min_price = storage.boxes.aggregate(Min('price'))
            storage.min_price = min_price['price__min']
        return self


class Storage(models.Model):
    numer = models.IntegerField(verbose_name='Номер склада')
    city = models.CharField(max_length=25, verbose_name='Город склада', blank=True)
    address = models.TextField(verbose_name='Адрес склада')
    feature = models.CharField(max_length=25, verbose_name='Особенность склада')
    image = models.ImageField(verbose_name='Фото склада', blank=True)

    objects = StorageQuerySet.as_manager()

    def __str__(self):
        return f'{self.numer} {self.address}'

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'


class Box(models.Model):
    name = models.CharField(max_length=25, verbose_name='Обозначение')
    storage = models.ForeignKey(Storage, verbose_name='Склад',
                                on_delete=models.CASCADE,
                                related_name='boxes')
    length = models.FloatField(verbose_name='Длина')
    width = models.FloatField(verbose_name='Ширина')
    height = models.FloatField(verbose_name='Высота')
    price = models.IntegerField(verbose_name='Цена')
    is_occupied = models.BooleanField(verbose_name='Занят', default=False)

    def __str__(self):
        return f'{self.name}({self.length}x{self.width}x{self.height} м)'

    class Meta:
        verbose_name = 'Бокс'
        verbose_name_plural = 'Боксы'


class Order(models.Model):
    client = models.ForeignKey(Client,
                               on_delete=models.CASCADE,
                               related_name='orders',
                               verbose_name='Клиент')
    created_at = models.DateTimeField(verbose_name='Создано',
                                      auto_now_add=True)
    box = models.ForeignKey(Box,
                            on_delete=models.CASCADE,
                            related_name='orders',
                            verbose_name='Бокс',
                            null=True,
                            blank=True)
    paid_with = models.DateField(verbose_name="Оплачено c",
                                 null=True,
                                 blank=True)
    price = models.IntegerField(verbose_name='Стоимость')

    size = models.CharField(max_length=50,
                            verbose_name='Размер',
                            null=True,
                            blank=True)

    @property
    def storage(self):
        return self.box.storage

    def __str__(self):
        return f'#{self.pk} {self.client} {self.storage} {self.box}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
