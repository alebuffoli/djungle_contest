from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from api.models import Prize, Contest


class Command(BaseCommand):
    help = 'Create random users'

    def handle(self, *args, **kwargs):
        prize = Prize.objects.create(code='five-percent_discount', perday=45, name='Sconto del 5%')

        Contest.objects.create(code=f'C0002',
                               name='Vinci uno sconto',
                               start='2020-02-01',
                               end='2020-02-29',
                               prize=prize)

        Contest.objects.create(code=f'C0001',
                               name='Vinci uno sconto',
                               start='2022-02-01',
                               end='2022-02-28',
                               prize=prize)

