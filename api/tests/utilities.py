from api.models import Prize, Contest, UserToContest
from datetime import datetime, timedelta, date
from django.utils import timezone
import pytest
from api.utilities import n_requests_estimate
from django.contrib.auth.models import User
from django.urls import reverse
url_auth = reverse('token_obtain_pair')


json_contest_not_active = {
    "error": {
        "status": "422",
        "title": "Contest is not active",
        "detail": "The contest with code C0002 is not active."
    }
}

json_contest_not_found = {
    "error": {
        "status": "404",
        "title": "Contest not found",
        "detail": "Contest code C9999 not found."
    }
}


@pytest.mark.django_db(transaction=True)
def create_contests():
    prize = Prize.objects.create(code='five-percent_discount', perday=45, name='Sconto del 5%')

    start = datetime.now(tz=timezone.get_current_timezone()).replace(day=1)
    end = last_day_of_month(start)

    Contest.objects.create(code=f'C0001',
                           name='Vinci uno sconto',
                           start=start,
                           end=end,
                           prize=prize)

    Contest.objects.create(code=f'C0002',
                           name='Vinci uno sconto',
                           start=start - timedelta(days=100),
                           end=end - timedelta(days=100),
                           prize=prize)

    Contest.objects.create(code=f'C0003',
                           name='Vinci uno sconto',
                           start=start,
                           end=end,
                           prize=prize,
                           auth_required=True)


def create_contest(wins_per_day, code, expired=False, auth_required=False, wmax_per_user=None):
    prize = Prize.objects.create(code='five-percent_discount', perday=wins_per_day, name='Sconto del 5%')

    start = date.today().replace(day=1)
    end = last_day_of_month(start)

    if expired:
        start -= timedelta(days=100)
        end -= timedelta(days=100)

    return Contest.objects.create(code=f'C{code}',
                                  name='Vinci uno sconto',
                                  start=start,
                                  end=end,
                                  prize=prize,
                                  auth_required=auth_required,
                                  wmax_per_user=wmax_per_user)


def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)


def run_multiple_contest(client, url, wins_per_day, contests):
    contests_failed = 0

    attempts_per_day = int(n_requests_estimate(wins_per_day))

    for c in range(1, contests + 1):
        code = str(c).zfill(4)
        create_contest(wins_per_day, code)
        url_complete = url + f'?contest=C{code}'
        winnings = 0
        for request in range(attempts_per_day):
            response = client.get(url_complete)
            winnings += 1 if response.json()['data']['winner'] else 0

        contests_failed += 1 if winnings != wins_per_day else 0
        is_ok = 'NOT OK' if winnings != wins_per_day else 'OK'
        print(f'CONTEST {c} ({is_ok}) {winnings} winnings out of {wins_per_day}, {attempts_per_day} attempts.')

    print(f'\n\nRan {contests} contests, {contests_failed} have not distribute all the prizes.\n\n')

    return contests_failed


def create_users():
    User.objects.create_user('user1', 'user1@gmail.com', 'testing321').save()
    User.objects.create_user('user2', 'user2@gmail.com', 'testing321').save()
    return User.objects.filter(username='user1').first()


def login_user(client):
    data = {"username": "user1", "password": "testing321"}
    return client.post(url_auth, data)


def login_user2(client):
    data = {"username": "user2", "password": "testing321"}
    return client.post(url_auth, data)


@pytest.mark.django_db(transaction=True)
def create_user_to_contest():
    user = create_users()
    contest = create_contest(10, '0003', expired=False, auth_required=True)
    UserToContest.objects.create(contest=contest, user=user)
    return contest


@pytest.mark.django_db(transaction=True)
def create_user_to_contest_wmax(wmax_per_user=2):
    user = create_users()
    contest = create_contest(10, '0003', expired=False, auth_required=True, wmax_per_user=wmax_per_user)
    UserToContest.objects.create(contest=contest, user=user)
    return contest
