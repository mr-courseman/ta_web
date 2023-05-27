from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Passport(models.Model):
    series = models.CharField(max_length=5, blank=False, null=False, verbose_name='Серия')
    number = models.CharField(max_length=7, blank=False, null=False, verbose_name='Номер')
    code = models.CharField(max_length=7, blank=False, null=False, verbose_name='Код подразделения')
    issue_date = models.DateField(null=False, verbose_name='Дата выдачи')
    giver = models.CharField(max_length=256, blank=False, null=False, verbose_name='Кем выдан')

    class Meta:
        db_table = 'Passport'
        verbose_name = 'Паспорт'
        verbose_name_plural = 'Паспорта'


class Client(User):
    patronymic = models.CharField(max_length=256, verbose_name='Отчество')
    phone = PhoneNumberField(unique=True, null=False, blank=False, verbose_name='Номер телефона')
    birthday = models.DateField(null=False, blank=False, verbose_name='Дата рождения')
    passport = models.ForeignKey('Passport', on_delete=models.CASCADE, verbose_name='Паспорт')

    def get_lfp(self):
        lfp = ('%s %s %s' % (self.last_name, self.first_name, self.patronymic))
        if lfp is None:
            return ''
        return lfp

    def get_phone(self):
        return self.phone.as_e164

    class Meta:
        db_table = 'Сlient'
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Personal(User):
    patronymic = models.CharField(max_length=256, verbose_name='Отчество')
    phone = PhoneNumberField(unique=True, null=False, blank=False, verbose_name='Номер телефона')

    def get_lfp(self):
        lfp = ('%s %s %s' % (self.last_name, self.first_name, self.patronymic))
        if lfp is None:
            return ''
        return lfp

    def get_phone(self):
        return self.phone.as_e164

    class Meta:
        db_table = 'Personal'
        verbose_name = 'Персонал'
        verbose_name_plural = 'Персонал'


TYPES = (
    (None, '------------'),
    ('Standard', 'Standard'),
    ('Bedroom', 'Bedroom'),
    ('Superior', 'Superior'),
    ('Family Room', 'Family Room'),
    ('Family Studio', 'Family Studio'),
    ('Suite', 'Suite'),
    ('Junior Suite', 'Junior Suite'),
    ('De Luxe', 'De Luxe'),
    ('Executive Suite', 'Executive Suite'),
    ('Business Room', 'Business Room'),
    ('Connected Room', 'Connected Room'),
    ('Duplex', 'Duplex'),
    ('Apartment', 'Apartment'),
    ('King Suite', 'King Suite'),
    ('President Suite', 'President Suite'),
)


class Place(models.Model):
    hotel = models.CharField(max_length=256, null=False, blank=False, verbose_name='Название отеля')
    name = models.CharField(choices=TYPES, max_length=256, null=False, blank=False, verbose_name='Тип апартаментов')
    count = models.IntegerField(null=False, verbose_name='Количество спальных мест')
    description = models.TextField(null=False, verbose_name='Описание')

    class Meta:
        db_table = 'Place'
        verbose_name = 'Место'
        verbose_name_plural = 'Места'


class Movement(models.Model):
    d_city = models.CharField(max_length=256, null=False, verbose_name='Город отправления')
    d_time = models.DateTimeField(null=False, blank=False, verbose_name='Время отправления')
    a_time = models.DateTimeField(null=False, blank=False, verbose_name='Время прибытия')
    a_city = models.CharField(max_length=256, null=False, verbose_name='Город прибытия')

    class Meta:
        db_table = 'Movement'
        verbose_name = 'Путешествие'
        verbose_name_plural = 'Путешествия'


class Tour(models.Model):
    nights = models.IntegerField(null=False, verbose_name='Количество дней')
    place = models.ForeignKey('Place', on_delete=models.CASCADE, verbose_name='Место')
    description = models.TextField(null=False, verbose_name='Описание тура')
    movement = models.ForeignKey('Movement', on_delete=models.CASCADE, verbose_name='Путешествие')
    cost = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Стоимость')

    class Meta:
        db_table = 'Tour'
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'


class Contract(models.Model):
    seller = models.ForeignKey('Personal', on_delete=models.CASCADE, verbose_name='Продавец')
    client = models.ForeignKey('Client', on_delete=models.CASCADE, verbose_name='Клиент')
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, verbose_name='Тур')
    time = models.DateTimeField(null=False, blank=False, verbose_name='Время и дата заключения')

    class Meta:
        db_table = 'Contract'
        verbose_name = 'Контракт'
        verbose_name_plural = 'Контракты'
