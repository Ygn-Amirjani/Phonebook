from conf.flaskConfig import CONFIG
from app import app as flask_app
import random
import string
import pytest
import json

HEADERS = {
    'Content-Type': 'application/json'
}

USER_MAIN_LINK = CONFIG.get('routes', {}).get('user', {}).get('main')
USERNAME_SELECT_FAIL = "YEGANE"
NEW_PHONE_NUMBER = "989100043286"
PHONE_NUMBER_NOT_FOR_USER = "989924776653"

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

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

USERNAME = make_username_random(10)
PHONE_NUMBER = f'989{make_phoneNumber_random(8)}'

def test_user_successfully_added(client):
    """ Test the insert class to see if a new user is added """

    data = {
        "username": USERNAME,
        "phoneNumber": PHONE_NUMBER
    }
    res = client.post(
        USER_MAIN_LINK,
        data = json.dumps(data),
        headers = HEADERS
    )

    assert res.status_code == 200

def test_user_not_added_successfully(client):
    """ Test the insert class to see if a duplicate user is added """

    data = {
        "username": USERNAME,
        "phoneNumber": PHONE_NUMBER
    }
    res = client.post(
        USER_MAIN_LINK,
        data = json.dumps(data),
        headers = HEADERS
    )

    assert res.status_code == 400

def test_user_successfully_updated(client):
    """ Test the update class to see if the phone number has been updated """

    data = {
        "username": USERNAME,
        "phoneNumber": PHONE_NUMBER
    }
    res = client.patch(
        f'{USER_MAIN_LINK}/{NEW_PHONE_NUMBER}',
        data = json.dumps(data),
        headers = HEADERS
    )

    assert res.status_code == 200

def test_there_is_no_user_with_this_phoneNumber(client):
    """ Test the update class to see if the missing phone number has been updated """

    data = {
        "username": USERNAME,
        "phoneNumber": PHONE_NUMBER_NOT_FOR_USER
    }
    res = client.patch(
        f'{USER_MAIN_LINK}/{NEW_PHONE_NUMBER}',
        data = json.dumps(data),
        headers = HEADERS
    )

    assert res.status_code == 400

def test_phone_numbers_are_same(client):
    """ Test the update class to see if the duplicate phone number is updated """

    data = {
        "username": USERNAME,
        "phoneNumber": PHONE_NUMBER
    }
    res = client.patch(
        f'{USER_MAIN_LINK}/{PHONE_NUMBER}',
        data = json.dumps(data),
        headers = HEADERS
    )

    assert res.status_code == 400

def test_user_found_successfully(client):
    """ Test the Select class to see if there is a user """

    res = client.get(
        f'{USER_MAIN_LINK}/{USERNAME}',
        headers = HEADERS
    )

    assert res.status_code == 200

def test_failed_find_user(client):
    """ Test the Select class to see if there is a user """

    resutl = client.get(
        f'{USER_MAIN_LINK}/{USERNAME_SELECT_FAIL}',
        headers = HEADERS
    )

    assert resutl.status_code == 404

def test_usernames_not_found_for_delete(client):
    """ Test the delete class to see if a user is deleted """

    data = {
        "username": USERNAME_SELECT_FAIL,
        "phoneNumber": PHONE_NUMBER
    }
    res = client.delete(
        USER_MAIN_LINK,
        data = json.dumps(data),
        headers = HEADERS
    )

    assert res.status_code == 400

def test_phoneNumber_not_found_for_delete(client):
    """ Test the delete class to see if a user is deleted """

    data = {
        "username": USERNAME,
        "phoneNumber": PHONE_NUMBER_NOT_FOR_USER
    }
    res = client.delete(
        USER_MAIN_LINK,
        data = json.dumps(data),
        headers = HEADERS
    )

    assert res.status_code == 400

def test_user_successfully_deleted(client):
    """ Test the delete class to see if a user is deleted """

    data = {
        "username": USERNAME,
        "phoneNumber": NEW_PHONE_NUMBER
    }
    res = client.delete(
        USER_MAIN_LINK,
        data = json.dumps(data),
        headers = HEADERS
    )

    assert res.status_code == 200

