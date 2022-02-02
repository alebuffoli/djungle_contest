from api.models import Prize, Contest
from datetime import datetime, timedelta, date
from django.utils import timezone
import pytest
from api.utilities import n_requests_estimate


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
        "detail": "Contest code C0003 not found."
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


def create_contest(wins_per_day, code, expired=False):
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
                                  prize=prize)


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
