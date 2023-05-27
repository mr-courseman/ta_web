from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission
import logging
from ...models import *

CREATE_PERMISSIONS = ['ta_web_models_add']
READ_PERMISSIONS = ['view']
UPDATE_PERMISSIONS = ['change']
DELETE_PERMISSIONS = ['delete']
RD_PERMISSIONS = ['view', 'delete']
RU_PERMISSIONS = ['view', 'change']
ALL_PERMISSIONS = ['ta_web_models_add', 'view', 'change', 'delete']

GROUPS = {
    'Django specific': {
        'log entry': ALL_PERMISSIONS,
        'group': ALL_PERMISSIONS,
        'permission': ALL_PERMISSIONS,
        'content type': ALL_PERMISSIONS,
        'session': ALL_PERMISSIONS,
        'user': ALL_PERMISSIONS,
    },

    'Admin': {
        'log entry': ALL_PERMISSIONS,
        'group': ALL_PERMISSIONS,
        'permission': ALL_PERMISSIONS,
        'content type': ALL_PERMISSIONS,
        'session': ALL_PERMISSIONS,
        'user': ALL_PERMISSIONS,
        'Паспорт': ALL_PERMISSIONS,
        'Клиент': ALL_PERMISSIONS,
        'Персонал': ALL_PERMISSIONS,
        'Место': ALL_PERMISSIONS,
        'Путешествие': ALL_PERMISSIONS,
        'Тур': ALL_PERMISSIONS,
        'Контракт': ALL_PERMISSIONS,
    },

    'Manager': {
        'Персонал': RU_PERMISSIONS,
        'Место': ALL_PERMISSIONS,
        'Путешествие': ALL_PERMISSIONS,
        'Тур': ALL_PERMISSIONS,
    },

    'Seller': {
        'Паспорт': ALL_PERMISSIONS,
        'Клиент': ALL_PERMISSIONS,
        'Персонал': RU_PERMISSIONS,
        'Место': READ_PERMISSIONS,
        'Путешествие': READ_PERMISSIONS,
        'Тур': READ_PERMISSIONS,
        'Контракт': ALL_PERMISSIONS,
    },

    'Client': {
        'Паспорт': RD_PERMISSIONS,
        'Клиент': RD_PERMISSIONS,
        'Место': READ_PERMISSIONS,
        'Путешествие': READ_PERMISSIONS,
        'Тур': READ_PERMISSIONS,
        'Контракт': READ_PERMISSIONS,
    },

}

PERSONAL = {
    'MegaEater42': ['Admin', 'Abobus1@mail.ru', 'ME42', 'Mega', 'Eater', '42', '+79192853791', True, True],
    'Wolf': ['Manager', 'Abobus2@mail.ru', 'wolf_wolf', 'Wolf', 'Wolfgang', 'Wolfovich', '+79192853792', False, False],
    'Sheep': ['Seller', 'Abobus3@mail.ru', 'sheep_sheep', 'Sheep', 'Sheepen', 'Sheepovich', '+79192853793', False, False],
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        # print(Permission.objects.all())
        for group_name in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group_name)
            # Loop models in group
            for app_model in GROUPS[group_name]:
                # Loop permissions in group/model
                for permission_name in GROUPS[group_name][app_model]:
                    # Generate permission name as Django would generate it
                    name = "Can {} {}".format(permission_name, app_model)
                    print("Creating {}".format(name))
                    try:
                        model_add_perm = Permission.objects.get(name=name)
                    except Permission.DoesNotExist:
                        logging.warning("Permission not found with name '{}'.".format(name))
                        continue
                    new_group.permissions.add(model_add_perm)
            for user in PERSONAL:
                if PERSONAL[user][0] == str(new_group):
                    new_user, created = Personal.objects.get_or_create(username=user,
                                                                       email=PERSONAL[user][1],
                                                                       first_name=PERSONAL[user][3],
                                                                       last_name=PERSONAL[user][4],
                                                                       patronymic=PERSONAL[user][5],
                                                                       phone=PERSONAL[user][6],
                                                                       is_superuser=PERSONAL[user][7],
                                                                       is_staff=PERSONAL[user][8],
                                                                       )
                    if created:
                        new_user.set_password(PERSONAL[user][2])
                        new_user.save()

                    new_group.user_set.add(new_user)
                    print("Adding {} to {}".format(user, new_group))
