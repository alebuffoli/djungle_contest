import pytest
from django.urls import reverse
from api.tests.utilities import n_requests_estimate, create_user_to_contest_wmax, login_user
from rest_framework.test import APIClient

url = reverse('play')


@pytest.mark.django_db
def test_run_contest_wmax_2(client):
    winnings = 0
    wmax_per_user = 2
    contest = create_user_to_contest_wmax(wmax_per_user=wmax_per_user)

    response = login_user(client)
    token = response.json()['access']

    param = '?contest=C0003&user_id=1'
    client = APIClient()

    attempts_per_day = int(n_requests_estimate(contest.prize.perday))

    for c in range(attempts_per_day):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = client.get(url + param)
        if winnings == wmax_per_user:
            assert response.status_code != 200
        elif response.json()['data']['winner'] is True:
            winnings += 1
            assert response.status_code == 200

    assert winnings == 2
