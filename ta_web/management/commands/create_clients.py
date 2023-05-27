from django.core.management import BaseCommand
from django.contrib.auth.models import Group
from ...models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        group = Group.objects.get(name='Client')
        for i in range(15, 30):
            new_passport = Passport.objects.create(
                series='7777',
                number=f'00000{i - 13}',
                code='123456',
                issue_date=f'2011-10-{i + 1}',
                giver='Каким-то отделением какого-то органа по какой-то области где-то'
            )
            new_user = Client.objects.create(username=f'Test{i - 13}',
                                             password='test_test',
                                             email=f'test{i - 13}@mail.ru',
                                             first_name=f'Тест{i - 13}',
                                             last_name=f'Тестовый{i - 13}',
                                             patronymic=f'Тестович{i - 13}',
                                             phone=f'+7900000000{i - 13}',
                                             birthday=f'1991-10-{i + 1}',
                                             passport=new_passport,
                                             is_superuser=False,
                                             is_staff=False,
                                             )
            group.user_set.add(new_user)
