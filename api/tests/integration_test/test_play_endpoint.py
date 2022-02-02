import pytest
from django.urls import reverse
from api.tests.utilities import create_contests, run_multiple_contest, json_contest_not_active, json_contest_not_found

url = reverse('play')


@pytest.mark.django_db
def test_no_param(client):
    response = client.get(url)
    assert response.status_code == 406


@pytest.mark.django_db
def test_wrong_param(client):
    param = '?contest_code=C0003'
    response = client.get(url + param)
    assert response.status_code == 406


@pytest.mark.django_db
def test_contest_not_found(client):
    create_contests()
    param = '?contest=C0003'
    response = client.get(url + param)
    assert response.status_code == 404
    assert response.json() == json_contest_not_found


@pytest.mark.django_db
def test_contest_not_active(client):
    create_contests()
    param = '?contest=C0002'
    response = client.get(url + param)
    assert response.status_code == 422
    assert response.json() == json_contest_not_active


@pytest.mark.django_db
def test_contest_active(client):
    create_contests()
    param = '?contest=C0001'
    response = client.get(url + param)
    assert response.status_code == 200


@pytest.mark.django_db
def test_contest_winning(client):
    contests_failed = run_multiple_contest(client, url, 45, 5)
    assert contests_failed <= 1


@pytest.mark.django_db
def test_real_contest(client, wins_per_day, contests):
    print(f'\n\n\n\n\n\n\nI will run {contests} contests.')
    print('######################### REAL LIFE EXAMPLE STARTED #########################\n\n')
    print('It may take a while..\n\n')
    run_multiple_contest(client, url, wins_per_day=int(wins_per_day), contests=int(contests))
    print('######################### END #########################')
