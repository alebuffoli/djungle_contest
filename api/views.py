from rest_framework.response import Response
from rest_framework.views import APIView
from api.utilities import get_code, get_contest, check_contest_validity, get_prizes_remaining, \
    is_prize_available, has_won, increase_total_winnings, increase_attempts, get_user_id, \
    check_contest_auth, can_win


class PlayView(APIView):

    def get(self, request):
        contest_code = get_code(request)
        user_id = get_user_id(request)

        contest = get_contest(contest_code)
        check_contest_validity(contest)
        check_contest_auth(contest, user_id)

        can_win(contest, user_id)

        win_per_day = get_prizes_remaining(contest)
        prize_available = is_prize_available(win_per_day, contest)

        if not prize_available or not has_won(contest, win_per_day, user_id):
            increase_attempts(win_per_day)
            content = {
                "data": {
                    "winner": False,
                    "prize": None
                }
            }
        else:
            increase_total_winnings(win_per_day)
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

