from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from api.models import Prize, Contest, UserToContest
from django.contrib.auth.models import User
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Create random users'

    def handle(self, *args, **kwargs):
        prize1 = Prize.objects.create(code='five-percent_discount', perday=45, name='Sconto del 5%')
        prize2 = Prize.objects.create(code='ten-percent_discount', perday=3, name='Sconto del 10%')

        start = date.today().replace(day=1)
        end = last_day_of_month(start)

        Contest.objects.create(code=f'C0001',
                               name='Vinci uno sconto',
                               start=start,
                               end=end,
                               prize=prize1)

        Contest.objects.create(code=f'C0002',
                               name='Vinci uno sconto',
                               start=start - timedelta(days=100),
                               end=end - timedelta(days=100),
                               prize=prize1)

        contest3 = Contest.objects.create(code=f'C0003',
                                          name='Vinci uno sconto',
                                          start=start,
                                          end=end,
                                          prize=prize2,
                                          auth_required=True,
                                          wmax_per_user=None)

        contest4 = Contest.objects.create(code=f'C0004',
                                          name='Vinci uno sconto',
                                          start=start,
                                          end=end,
                                          prize=prize2,
                                          auth_required=True,
                                          wmax_per_user=2)

        User.objects.create_user('user1', 'user1@gmail.com', 'testing321').save()
        User.objects.create_user('user2', 'user2@gmail.com', 'testing321').save()

        User.objects.create_superuser('admin', 'admin@admin.com', 'admin').save()

        user1 = User.objects.filter(username='user1').first()

        UserToContest.objects.create(contest=contest3, user=user1)
        UserToContest.objects.create(contest=contest4, user=user1)


def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)