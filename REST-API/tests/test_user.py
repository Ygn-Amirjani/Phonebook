from ..conf.flaskConfig import CONFIG
import json
import random
import string

HEADERS = {
    'Content-Type': 'application/json'
}

USER_MAIN_LINK = CONFIG.get('routes', {}).get('user', {}).get('main')

def make_username_random(length: int) -> str:
    random_username = ''.join(
        random.choice(string.ascii_lowercase) for _ in range(length)
    )

    return random_username

def make_phoneNumber_random(length: int) -> str:
    random_phoneNumber = ''.join(
        str(random.choice([0,1,2,3,4,5,6,7,8,9])) for i in range(length)
    )

    return random_phoneNumber

USERNAME = make_username_random(10)
PHONE_NUMBER = f'989{make_phoneNumber_random(8)}'

def test_user_successfully_added(app, client):
    """ Test the insert class to see if a new user is added """

    data = {
        "username": USERNAME,
        "phoneNumber": PHONE_NUMBER
    }
    result = client.post(
        USER_MAIN_LINK,
        data = json.dumps(data),
        headers = HEADERS
    )

    assert result.status_code == 200

def test_user_not_added_successfully(app, client):
    """ Test the insert class to see if a duplicate user is added """

    data = {
        "username": USERNAME,
        "phoneNumber": PHONE_NUMBER
    }
    result = client.post(
        USER_MAIN_LINK,
        data = json.dumps(data),
        headers = HEADERS
    )

    assert result.status_code == 400

# def test_user_successfully_updated(app, client):

def test_user_found_successfully(client):
    """ Test the Select class to see if there is a user """

    result = client.get(
        f'{USER_MAIN_LINK}/{USERNAME}',
        headers = HEADERS
    )

    assert result.status_code == 200

def test_failed_find_user(client):
    """ Test the Select class to see if there is a user """

    resutl = client.get(
        f'{USER_MAIN_LINK}/YEGANE',
        headers = HEADERS
    )

    assert resutl.status_code == 404
