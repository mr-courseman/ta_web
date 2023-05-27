from django.core.management import BaseCommand
from ...models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(2, 8):
            new_place = Place.objects.create(
                count=i,
                name=TYPES[i],
                hotel=f'Какой-то классный отель №{i}',
                description=f'Описание какого-то классного тура №{i}',
            )

            new_movement = Movement.objects.create(
                d_city=f'Какой-то город №{i}',
                d_time=f'2023-07-0{i} 0{i}:0{i}:00+03',
                a_city=f'Другой город №{i}',
                a_time=f'2023-07-0{i + 1} 0{i + 1}:0{i + 1}:00+03',
            )

            new_tour = Tour.objects.create(
                place=new_place,
                nights=f'{i}',
                cost=f'{i}0000.0{i}',
                movement=new_movement,
                description=f'Описание какого-то классного тура №{i}',
            )
