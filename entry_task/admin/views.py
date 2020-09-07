from django.http import HttpResponse
import datetime
import sys, os, django
sys.path.append("/entry_task")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "entry_task.settings")
django.setup()
from django.conf import settings

from django.shortcuts import render
from api.api import user, event, photo
import json


def login(request):
    if request.POST.get('username', None) is not None and request.POST.get('password', None):
        res = user.login(request)
        json_obj = json.loads(res.content)
        access_token = json_obj.get('access_token', None)
        if access_token is None:
            return render(request, 'login.html', {'title': 'Login', 'result': 'Incorrect username or password'})
        else:
            response = render(request, 'login.html', {'token': access_token})
            set_cookie(response, 'user', access_token, 1)
            return response
    else:
        return render(request, 'login.html')


def create_event(request):
    token = request.COOKIES.get('user')
    if request.POST:
        request.META['HTTP_AUTHORIZATION'] = 'Bearer ' + token
        res = event.event(request)
        json_obj = json.loads(res.content)
        return render(request, 'create_event.html', {'title': 'Create Event', 'result': json_obj['result'], 'token': token})
    return render(request, 'create_event.html', {'title': 'Create Event', 'token': token})


def upload(request):
    token = request.COOKIES.get('user')
    if request.POST:
        request.META['HTTP_AUTHORIZATION'] = 'Bearer ' + token
        res = photo.upload(request)
        json_obj = json.loads(res.content)
        return render(request, 'upload.html',
                      {'title': 'Upload Image', 'result': json_obj['result'], 'token': token, 'image': 'http://' + json_obj['detail'][0]})
    return render(request, 'upload.html', {'title': 'Upload Image', 'token': token})


def update(request):
    token = request.COOKIES.get('user')
    request = request.copy()
    if request.POST:
        request.META['HTTP_AUTHORIZATION'] = 'Bearer ' + token

        res = event.update_event(request, request.POST['event_id'])
        json_obj = json.loads(res.content)
        return render(request, 'update.html',
                      {'title': 'Update Event', 'result': json_obj['result'], 'token': token})
    return render(request, 'update.html', {'title': 'Update Event', 'token': token})


def set_cookie(response, key, value, hour_expired):
    max_age = hour_expired * 60 * 60
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)
