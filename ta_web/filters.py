from django.forms import DateInput, TimeInput
from django_filters import FilterSet, CharFilter, DateFilter, TimeFilter

from ta_web.models import Client


# class ContactFilter(FilterSet):
#     first_name = CharFilter(field_name='first_name', lookup_expr='icontains', label='Имя')
#     last_name = CharFilter(field_name='last_name', lookup_expr='icontains', label='Фамилия')
#     middle_name = CharFilter(field_name='middle_name', lookup_expr='icontains', label='Отчество')
#
#     class Meta:
#         model = Contacts
#         fields = ('first_name', 'last_name', 'middle_name', 'phone')


class LFPFilter(FilterSet):
    last_name = CharFilter(field_name='last_name', lookup_expr='icontains')
    first_name = CharFilter(field_name='first_name', lookup_expr='icontains')
    patronymic = CharFilter(field_name='patronymic', lookup_expr='icontains')

    class Meta:
        model = Client
        fields = ('last_name', 'first_name', 'patronymic')
