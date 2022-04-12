from ..conf.flaskConfig import CONFIG
import json
import random
import string

HEADERS = {
    'Content-Type': 'application/json'
}

USER_MAIN_LINK = CONFIG.get('routes', {}).get('user', {}).get('main')
USERNAME_SELECT_FAIL = ""
NEW_PHONE_NUMBER = ""
PHONE_NUMBER_NOT_FOR_USER = ""

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

def test_user_successfully_updated(app, client):
    """ Test the update class to see if the phone number has been updated """

    data = {
        "username": USERNAME,
        "phoneNumber": PHONE_NUMBER
    }
    result = client.patch(
        f'{USER_MAIN_LINK}/{NEW_PHONE_NUMBER}',
        data = json.dumps(data),
        headers = HEADERS
    )

    assert result.status_code == 200

def test_there_is_no_user_with_this_phoneNumber(app, client):
    """ Test the update class to see if the missing phone number has been updated """

    data = {
        "username": USERNAME,
        "phoneNumber": PHONE_NUMBER_NOT_FOR_USER
    }
    result = client.patch(
        f'{USER_MAIN_LINK}/{NEW_PHONE_NUMBER}',
        data = json.dumps(data),
        headers = HEADERS
    )

    assert result.status_code == 400

def test_phone_numbers_are_same(app, client):
    """ Test the update class to see if the duplicate phone number is updated """

    data = {
        "username": USERNAME,
        "phoneNumber": PHONE_NUMBER
    }
    result = client.patch(
        f'{USER_MAIN_LINK}/{PHONE_NUMBER}',
        data = json.dumps(data),
        headers = HEADERS
    )

    assert result.status_code == 400

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
        f'{USER_MAIN_LINK}/{USERNAME_SELECT_FAIL}',
        headers = HEADERS
    )

    assert resutl.status_code == 404

def test_user_successfully_deleted(app, client):
    """ Test the delete class to see if a user is deleted """

    data = {
        "username": USERNAME,
        "phoneNumber": PHONE_NUMBER
    }
    result = client.delete(
        USER_MAIN_LINK,
        data = json.dumps(data),
        headers = HEADERS
    )

    assert result.status_code == 200

def test_user_not_deleted_successfully(app, client):
    """ Test the delete class to see if a user is deleted """

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
