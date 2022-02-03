import pytest
from django.urls import reverse
from api.tests.utilities import create_contests, \
    create_users, create_user_to_contest, login_user, login_user2, n_requests_estimate
from rest_framework.test import APIClient

url = reverse('play')


@pytest.mark.django_db
def test_no_param(client):
    response = client.get(url)
    assert response.status_code == 406


@pytest.mark.django_db
def test_auth(client):
    create_users()
    response = login_user(client)
    assert response.status_code == 200


@pytest.mark.django_db
def test_wrong_auth(client):
    response = login_user(client)
    assert response.status_code == 401


@pytest.mark.django_db
def test_contest_with_auth_and_no_user(client):
    create_contests()
    param = '?contest=C0003'
    response = client.get(url + param)
    assert response.status_code == 403


@pytest.mark.django_db
def test_contest_with_auth(client):
    create_user_to_contest()

    response = login_user(client)

    param = '?contest=C0003&user_id=1'
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.json()['access']}")
    response = client.get(url + param)
    assert response.status_code == 200


@pytest.mark.django_db
def test_contest_with_auth_wrong_id(client):
    create_user_to_contest()

    response = login_user(client)

    param = '?contest=C0003&user_id=2'
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.json()['access']}")
    response = client.get(url + param)
    assert response.status_code == 401


@pytest.mark.django_db
def test_contest_with_auth_wrong_user(client):
    create_user_to_contest()

    response = login_user2(client)

    param = '?contest=C0003&user_id=2'
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.json()['access']}")
    response = client.get(url + param)
    assert response.status_code == 403


@pytest.mark.django_db
def test_run_contest(client):
    winnings = 0
    contest = create_user_to_contest()

    response = login_user(client)
    token = response.json()['access']

    param = '?contest=C0003&user_id=1'
    client = APIClient()

    attempts_per_day = int(n_requests_estimate(contest.prize.perday))

    for c in range(attempts_per_day):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = client.get(url + param)
        if response.json()['data']['winner'] is True:
            winnings += 1

    assert winnings > contest.prize.perday * 0.8
