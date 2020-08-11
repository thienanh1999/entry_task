import requests
import datetime
import random


# TODO: script to create superuser and 3 category


superuser = 'athen'
superpassword = '1'

NUMBER_OF_EVENTS = 1000000
NUMBER_OF_USER = 1000000
NUMBSER_OF_LIKE = 1000000
NUMBSER_OF_PARTICIPANT = 1000000
NUMBSER_OF_COMMENT = 1000000


def create_users():
    # Create User
    url = 'http://localhost:8000/api/create_user/'
    body = {
        'password': 1,
    }
    for i in range(NUMBER_OF_USER):
        username = 'user' + str(i)
        fullname = 'Vu Thi Thien Anh - ' + str(i)
        body['username'] = username
        body['fullname'] = fullname
        response = requests.post(url, data=body)
        print "Created " + str(i+1) + " users."


def get_access_token(username, password):
    url = 'http://localhost:8000/api/login/'
    body = {
        'username': username,
        'password': password,
    }
    response = requests.post(url, data=body)
    return response.json().get('access_token', '')


def create_event():
    url = 'http://localhost:8000/api/event/'
    body = {
        'title': 'title',
        'start': datetime.datetime.utcnow(),
        'end': datetime.datetime.utcnow(),
        'location': 'location',
        'category': '1,2,3',
    }
    header = {
        'Authorization': 'Bearer ' + get_access_token(superuser, superpassword)
    }

    for i in range(NUMBER_OF_EVENTS):
        body['title'] = 'title ' + str(i)
        response = requests.post(url, data=body, headers=header)
        print "Created " + str(i+1) + " events."


def create_like():
    url = 'http://localhost:8000/api/event/'
    for i in range(NUMBSER_OF_LIKE):
        user = random.randint(0, NUMBER_OF_USER-1)
        event = random.randint(0, NUMBER_OF_EVENTS-1)
        url1 = url + str(event) + "/like/"
        user = 'user' + str(user)
        header = {
            'Authorization': 'Bearer ' + get_access_token(user, '1')
        }
        response = requests.post(url1, headers=header)
        print "Liked " + str(i+1) + " times."


def create_participant():
    url = 'http://localhost:8000/api/event/'
    for i in range(NUMBSER_OF_PARTICIPANT):
        user = random.randint(0, NUMBER_OF_USER - 1)
        event = random.randint(0, NUMBER_OF_EVENTS - 1)
        url1 = url + str(event) + "/participant/"
        user = 'user' + str(user)
        header = {
            'Authorization': 'Bearer ' + get_access_token(user, '1')
        }
        response = requests.post(url1, headers=header)
        print "Participated " + str(i + 1) + " times."


def create_comment():
    url = 'http://localhost:8000/api/event/'
    body = {
        'comment': 'comment'
    }
    for i in range(NUMBSER_OF_COMMENT):
        user = random.randint(0, NUMBER_OF_USER - 1)
        event = random.randint(0, NUMBER_OF_EVENTS - 1)
        url1 = url + str(event) + "/comment/"
        user = 'user' + str(user)
        header = {
            'Authorization': 'Bearer ' + get_access_token(user, '1')
        }
        response = requests.post(url1, headers=header, data=body)
        print "Commented " + str(i + 1) + " times."


if __name__ == '__main__':
    create_users()
    create_event()
    create_like()
    create_participant()
    create_comment()
