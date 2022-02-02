from api.models import Contest, WinPerDay
from djungle_contest import api_exception
from datetime import date
import random
import math


def get_code(request):
    try:
        return request.GET['contest']
    except Exception:
        raise api_exception.ContestCodeRequiredException()


def get_contest(contest_code):
    try:
        return Contest.objects.get(code=contest_code)
    except Contest.DoesNotExist:
        raise api_exception.ContestNotFoundException(contest_code)


def check_contest_validity(contest):
    now = date.today()
    if not contest.start <= now <= contest.end:
        raise api_exception.ContestNotActiveException(contest.code)


def get_prizes_remaining(contest):
    win_per_day = WinPerDay.objects.filter(contest__code=contest.code, day=date.today()).first()
    if not win_per_day:
        win_per_day = WinPerDay.objects.create(day=date.today(), contest=contest)
    return win_per_day


def is_prize_available(win_per_day, contest):
    if not win_per_day:
        return True
    elif win_per_day.winnings < contest.prize.perday:
        return True

    return False


def probability_to_win(contest):
    requests_h = n_requests_estimate(contest.prize.perday) / 24
    prizes_h = contest.prize.perday / 24
    probability = prizes_h / requests_h
    return probability


def has_won(contest, win_per_day):
    probability = probability_to_win(contest)
    occasion = random.random()
    boost = 0

    if win_per_day.attempts > n_requests_estimate(contest.prize.perday) * 0.9 and win_per_day.winnings < contest.prize.perday:
        boost = 0.2

    return occasion - boost < probability


def increase_winnings(win_per_day):
    win_per_day.winnings += 1
    win_per_day.attempts += 1
    win_per_day.save()


def increase_attempts(win_per_day):
    win_per_day.attempts += 1
    win_per_day.save()


def n_requests_estimate(winnings):
    return math.pow(winnings, 3)
