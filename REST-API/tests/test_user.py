import json
import random
import string

# Load config file
with open('./conf/config.json', mode='r') as config_file:
    CONFIG = json.load(config_file)

HEADERS = {
    'Content-Type': 'application/json'
}

USER_SELECT = CONFIG.get('routes', {}).get('user', {}).get('select')
USER_INSERT = CONFIG.get('routes', {}).get('user', {}).get('insert')
USER_DELETE = CONFIG.get('routes', {}).get('user', {}).get('delete')
USER_UPDATE = CONFIG.get('routes', {}).get('user', {}).get('update')

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
        USER_INSERT,
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
        USER_INSERT,
        data = json.dumps(data),
        headers = HEADERS
    )

    assert result.status_code == 400

