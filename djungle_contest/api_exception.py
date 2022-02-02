from rest_framework.exceptions import APIException
from rest_framework import status


class ContestCodeRequiredException(APIException):
    def __init__(self):
        ContestCodeRequiredException.status_code = status.HTTP_406_NOT_ACCEPTABLE
        ContestCodeRequiredException.detail = {
            "error": {
                "status": f'{status.HTTP_406_NOT_ACCEPTABLE}',
                "title": 'Contest code required',
                "detail": f'Please provide a contest code.'
            }
        }


class ContestNotFoundException(APIException):
    def __init__(self, contest_code):
        ContestNotFoundException.status_code = status.HTTP_404_NOT_FOUND
        ContestNotFoundException.detail = {
            "error": {
                "status": f'{status.HTTP_404_NOT_FOUND}',
                "title": 'Contest not found',
                "detail": f'Contest code {contest_code} not found.'
            }
        }


class ContestNotActiveException(APIException):
    def __init__(self, contest_code):
        ContestNotActiveException.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        ContestNotActiveException.detail = {
            "error": {
                "status": f'{status.HTTP_422_UNPROCESSABLE_ENTITY}',
                "title": 'Contest is not active',
                "detail": f'The contest with code {contest_code} is not active.'
            }
        }
