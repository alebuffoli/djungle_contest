from rest_framework.response import Response
from rest_framework.views import APIView
from api.utilities import get_code, get_contest, check_contest_validity, get_prizes_remaining, \
    is_prize_available, has_won, increase_winnings, increase_attempts


class PlayView(APIView):

    def get(self, request):
        contest_code = get_code(request)
        contest = get_contest(contest_code)
        check_contest_validity(contest)

        win_per_day = get_prizes_remaining(contest)
        prize_available = is_prize_available(win_per_day, contest)

        if not prize_available or not has_won(contest, win_per_day):
            increase_attempts(win_per_day)
            content = {
                "data": {
                    "winner": False,
                    "prize": None
                }
            }
        else:
            increase_winnings(win_per_day)
            content = {
                "data": {
                    "winner": True,
                    "prize": {
                        "code": contest.prize.code,
                        "name": contest.prize.name
                    }
                }
            }

        return Response(content)

