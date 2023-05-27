import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .models import *


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'login'})
    )

    email = forms.EmailField(
        label='Email',
        max_length=256,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email'})
    )

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password1'})
    )

    password2 = forms.CharField(
        label='Повтор пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password2'})
    )

    phone = forms.CharField(
        label='Мобильный телефон',
        widget=PhoneNumberPrefixWidget(attrs={
            'class': 'form-control',
            'id': 'phone',
            },
            initial='RU',
            country_attrs={'id': 'phone_0'},
            number_attrs={'id': 'phone1'}
        )
    )

    first_name = forms.CharField(
        label='Имя',
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'name'})
    )

    last_name = forms.CharField(
        label='Фамилия',
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'lName'})
    )

    patronymic = forms.CharField(
        label='Отчество',
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'patronymic'})
    )

    birthday = forms.DateField(
        label='Дата рождения',
        widget=forms.DateInput(attrs={'class': 'form-control', 'id': 'birthday'})
    )

    series = forms.CharField(
        label='Серия пасспорта',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'series',
            'type': 'number',
            'maxlength': 4,
            'oninput': 'maxLengthCheck(this)'
        })
    )

    number = forms.CharField(
        label='Номер паспорта',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'number',
            'type': 'number',
            'maxlength': 6,
            'oninput': 'maxLengthCheck(this)'
        })
    )

    code = forms.CharField(
        label='Код подразделения',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'code',
            'type': 'number',
            'maxlength': 6,
            'oninput': 'maxLengthCheck(this)'
        })
    )

    issue_date = forms.DateField(
        label='Дата выдачи',
        widget=forms.DateInput(attrs={'class': 'form-control', 'id': 'issue_date'})
    )

    giver = forms.CharField(
        label='Кем выдан',
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'giver'})
    )

    passport = forms.CharField(
        label='',
        max_length=256,
        required=False,
        widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'passport'})
    )

    class Meta:
        model = Client
        fields = ('username', 'email', 'password1',
                  'password2', 'phone', 'first_name',
                  'last_name', 'patronymic', 'birthday', 'passport')

    def clean(self):
        if not self._errors:
            cleaned_data = super(RegisterUserForm, self).clean()
            email = cleaned_data.get('email')
            phone = cleaned_data.get('phone')
            series = cleaned_data.get('series')
            number = cleaned_data.get('number')
            code = cleaned_data.get('code')
            try:
                try:
                    int(series)
                    int(number)
                    int(code)
                except ValueError:
                    raise forms.ValidationError(u'ВОТ СКАЖИ, ЗАЧЕМ ТЫ \'-\' ВВОДИШЬ, А? ПУСЬКА ТЫ!')
                if User.objects.filter(email=email).exists():
                    raise forms.ValidationError(u'Пользователь с таким e-mail уже существует.')
                elif Client.objects.filter(phone=phone).exists():
                    raise forms.ValidationError(u'Пользователь с таким телефоном уже существует.')
                elif Passport.objects.filter(series=series, number=number, code=code).exists():
                    raise forms.ValidationError(u'Пользователь с такими пасспортными данными уже существует.')
            finally:
                try:
                    cleaned_data['passport'] = Passport.objects.create(series=series,
                                                                       number=number,
                                                                       code=code,
                                                                       issue_date=cleaned_data.get('issue_date'),
                                                                       giver=cleaned_data.get('giver'))
                finally:
                    return cleaned_data


class RegisterPersonalForm(UserCreationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'login'})
    )

    email = forms.EmailField(
        label='Email',
        max_length=256,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email'})
    )

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password1'})
    )

    password2 = forms.CharField(
        label='Повтор пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password2'})
    )

    phone = forms.CharField(
        label='Мобильный телефон',
        widget=PhoneNumberPrefixWidget(attrs={
                'class': 'form-control',
                'id': 'phone'
            },
            initial='RU',
            country_attrs={'id': 'phone_0'},
            number_attrs={'id': 'phone1'}
        )
    )

    first_name = forms.CharField(
        label='Имя',
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'name'})
    )

    last_name = forms.CharField(
        label='Фамилия',
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'lName'})
    )

    patronymic = forms.CharField(
        label='Отчество',
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'patronymic'})
    )

    class Meta:
        model = Personal
        fields = ('username', 'email', 'password1',
                  'password2', 'phone', 'first_name',
                  'last_name', 'patronymic')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'login'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password'})
    )


class ClientForm(ModelForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'login'})
    )

    email = forms.EmailField(
        label='Email',
        max_length=256,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email'})
    )

    phone = forms.CharField(
        label='Мобильный телефон',
        widget=PhoneNumberPrefixWidget(attrs={
                'class': 'form-control',
                'id': 'phone'
            },
            initial='RU',
            country_attrs={'id': 'phone_0'},
            number_attrs={'id': 'phone1'})
    )

    first_name = forms.CharField(
        label='Имя',
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'name'})
    )

    last_name = forms.CharField(
        label='Фамилия',
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'lName'})
    )

    patronymic = forms.CharField(
        label='Отчество',
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'patronymic'})
    )

    birthday = forms.DateField(
        label='Дата рождения',
        widget=forms.DateInput(attrs={'class': 'form-control', 'id': 'birthday'})
    )

    series = forms.CharField(
        label='Серия пасспорта',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'series',
            'type': 'number',
            'maxlength': 4,
            'oninput': 'maxLengthCheck(this)'
        })
    )

    number = forms.CharField(
        label='Номер паспорта',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'series',
            'type': 'number',
            'maxlength': 6,
            'oninput': 'maxLengthCheck(this)'
        })
    )

    code = forms.CharField(
        label='Код подразделения',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'code',
            'type': 'number',
            'maxlength': 6,
            'oninput': 'maxLengthCheck(this)'
        })
    )

    issue_date = forms.DateField(
        label='Дата выдачи',
        widget=forms.DateInput(attrs={'class': 'form-control', 'id': 'issue_date'})
    )

    giver = forms.CharField(
        label='Кем выдан',
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'giver'})
    )

    class Meta:
        model = Client
        fields = ('username', 'email', 'phone',
                  'first_name', 'last_name', 'patronymic',
                  'birthday')


def get_client_form(client):
    return ClientForm(initial={
        'username': client.username,
        'email': client.email,
        'phone': client.phone,
        'first_name': client.first_name,
        'last_name': client.last_name,
        'patronymic': client.patronymic,
        'birthday': client.birthday,
        'series': client.passport.series,
        'number': client.passport.number,
        'code': client.passport.code,
        'issue_date': client.passport.issue_date,
        'giver': client.passport.giver,
    })


class PersonalForm(ModelForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'login'})
    )

    email = forms.EmailField(
        label='Email',
        max_length=256,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email'})
    )

    phone = forms.CharField(
        label='Мобильный телефон',
        widget=PhoneNumberPrefixWidget(attrs={
            'class': 'form-control',
            'id': 'phone',
        },
            initial='RU',
            country_attrs={'id': 'phone_0'},
            number_attrs={'id': 'phone1'}
        )
    )

    first_name = forms.CharField(
        label='Имя',
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'name'})
    )

    last_name = forms.CharField(
        label='Фамилия',
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'lName'})
    )

    patronymic = forms.CharField(
        label='Отчество',
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'patronymic'})
    )

    class Meta:
        model = Personal
        fields = ('username', 'email', 'phone',
                  'first_name', 'last_name', 'patronymic')


class PlaceForm(ModelForm):
    hotel = forms.CharField(
        label='Название отеля',
        max_length=256,
        widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'hotel'})
    )

    name = forms.CharField(
        label='Тип апартаментов',
        max_length=256,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'name', 'choices': TYPES})
    )

    count = forms.IntegerField(
        label='Количество спальных мест',
        step_size=1,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'count'})
    )

    description = forms.CharField(
        label='Описание',
        widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'description'})
    )

    class Meta:
        model = Place
        fields = ('hotel', 'name', 'count', 'description')


class MovementForm(ModelForm):
    d_city = forms.CharField(
        label='Город отправления',
        max_length=256,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'd_city'})
    )

    d_time = forms.DateTimeField(
        label='Время отправления',
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'id': 'd_time'})
    )

    a_time = forms.DateTimeField(
        label='Время путешествия',
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'id': 'a_time'})
    )

    a_city = forms.CharField(
        label='Город прибытия',
        max_length=256,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'a_city'})
    )

    class Meta:
        model = Movement
        fields = ('d_city', 'd_time', 'a_time', 'a_city')


class TourForm(ModelForm):
    nights = forms.IntegerField(
        label='Количество ночей',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'nights',
            'type': 'number',
            'maxlength': 5,
            'oninput': 'maxLengthCheck(this)'
        })
    )

    hotel = forms.CharField(
        label='Название отеля',
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'hotel'})
    )

    name = forms.CharField(
        label='Тип апартаментов',
        max_length=256,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'name'}, choices=TYPES)
    )

    count = forms.IntegerField(
        label='Количество спальных мест',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'count',
            'type': 'number',
            'maxlength': 5,
            'oninput': 'maxLengthCheck(this)'
        })
    )

    hotel_description = forms.CharField(
        label='Описание отеля',
        widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'hotel_description'})
    )

    description = forms.CharField(
        label='Описание тура',
        widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'description'})
    )

    d_city = forms.CharField(
        label='Город отправления',
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'd_city'})
    )

    d_time = forms.DateTimeField(
        label='Время отправления',
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'id': 'd_time'})
    )

    a_time = forms.DateTimeField(
        label='Время прибытия',
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'id': 'a_time'})
    )

    a_city = forms.CharField(
        label='Город прибытия',
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'a_city'})
    )

    cost = forms.DecimalField(
        label='Стоимость',
        max_digits=15,
        decimal_places=2,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'cost', 'step': 0.01})
    )

    movement = forms.CharField(
        label='',
        required=False,
        widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'movement'})
    )

    place = forms.CharField(
        label='',
        required=False,
        widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'place'})
    )

    class Meta:
        model = Tour
        fields = ('nights', 'description', 'cost', 'movement', 'place')

    def clean(self):
        if not self._errors:
            cleaned_data = super(TourForm, self).clean()
            nights = cleaned_data.get('nights')
            cost = cleaned_data.get('cost')
            count = cleaned_data.get('count')

            try:
                try:
                    int(count)
                    int(nights)
                except ValueError:
                    raise forms.ValidationError(u'ВОТ СКАЖИ, ЗАЧЕМ ТЫ \'-\' ВВОДИШЬ, А? ПУСЬКА ТЫ!')
                if float(cost) < 0:
                    raise forms.ValidationError(u'ВОТ СКАЖИ, ЗАЧЕМ ТЫ \'-\' ВВОДИШЬ, А? ПУСЬКА ТЫ!')
            finally:
                try:
                    cleaned_data['place'], created = Place.objects.get_or_create(hotel=cleaned_data.get('hotel'),
                                                                                 name=cleaned_data.get('name'),
                                                                                 description=cleaned_data.get('hotel_description'),
                                                                                 count=count)

                    cleaned_data['movement'], created = Movement.objects.get_or_create(a_time=cleaned_data.get('a_time'),
                                                                                       a_city=cleaned_data.get('a_city'),
                                                                                       d_time=cleaned_data.get('d_time'),
                                                                                       d_city=cleaned_data.get('d_city'))
                finally:
                    return cleaned_data


def get_tour_form(tour):
    return TourForm(initial={
        'nights': tour.nights,
        'description': tour.description,
        'cost': tour.cost,
        'hotel': tour.place.hotel,
        'name': tour.place.name,
        'count': tour.place.count,
        'hotel_description': tour.place.description,
        'd_city': tour.movement.d_city,
        'd_time': tour.movement.d_time,
        'a_time': tour.movement.a_time,
        'a_city': tour.movement.a_city,
    })


class ContractForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tour'].queryset = Tour.objects.all()
        self.fields['seller'].queryset = Personal.objects.filter(groups__name='Seller')
        self.fields['client'].queryset = Client.objects.all()

    seller = forms.ModelChoiceField(
        label='Продавец',
        queryset=None,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'mSel', })
    )

    client = forms.ModelChoiceField(
        label='Клиент',
        queryset=None,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'mSel'})
    )

    tour = forms.ModelChoiceField(
        label='Тур',
        queryset=None,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'mSel'})
    )

    time = forms.DateTimeField(
        label='',
        required=False,
        widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'time'})
    )

    class Meta:
        model = Contract
        fields = ('seller', 'client', 'tour', 'time')

    def clean(self):
        if not self._errors:
            cleaned_data = super(ContractForm, self).clean()
            cleaned_data['time'] = datetime.datetime.now()

            return cleaned_data
