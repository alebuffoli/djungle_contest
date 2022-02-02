import pytest


def pytest_addoption(parser):
    parser.addoption("--wins_per_day", action="store")
    parser.addoption("--contests", action="store")


@pytest.fixture(scope='session')
def wins_per_day(request):
    value = request.config.option.wins_per_day
    if value is None:
        pytest.skip()
    return value


@pytest.fixture(scope='session')
def contests(request):
    value = request.config.option.contests
    if value is None:
        pytest.skip()
    return value
