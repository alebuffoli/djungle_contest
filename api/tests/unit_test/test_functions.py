import pytest
from api.models import Contest
from api.tests.utilities import create_contest
from api.utilities import get_contest, check_contest_validity, get_prizes_remaining, \
    is_prize_available, has_won, increase_total_winnings, probability_to_win
from djungle_contest.api_exception import ContestNotActiveException, ContestNotFoundException

code = str(1).zfill(4)


@pytest.mark.django_db
def test_get_contest():
    create_contest(45, code)
    c = get_contest(f'C{code}')
    assert type(c) == Contest
    assert c.code == f'C{code}'


@pytest.mark.django_db
def test_get_wrong_contest():
    create_contest(45, code)
    with pytest.raises(ContestNotFoundException) as e:
        get_contest(f'C0002')

    assert e.type == ContestNotFoundException


@pytest.mark.django_db
# This test should not raise any exception
def test_contest_valid():
    contest = create_contest(45, code)
    check_contest_validity(contest)


@pytest.mark.django_db
def test_contest_not_valid():
    contest = create_contest(45, code, expired=True)
    with pytest.raises(ContestNotActiveException) as e:
        check_contest_validity(contest)

    assert e.type == ContestNotActiveException


@pytest.mark.django_db
def test_prize_available():
    contest = create_contest(45, code)
    win_per_day = get_prizes_remaining(contest)
    assert is_prize_available(win_per_day, contest) is True


@pytest.mark.django_db
def test_prize_not_available():
    contest = create_contest(45, code)
    win_per_day = get_prizes_remaining(contest)
    for w in range(45):
        increase_total_winnings(win_per_day)
    win_per_day = get_prizes_remaining(contest)

    assert is_prize_available(win_per_day, contest) is False


@pytest.mark.django_db
def test_probability():
    contest = create_contest(1, code)
    probability = probability_to_win(contest)
    assert probability <= 1


@pytest.mark.django_db
def test_has_won():
    contest = create_contest(1, code)
    win_per_day = get_prizes_remaining(contest)
    assert type(has_won(contest, win_per_day, None)) == bool


