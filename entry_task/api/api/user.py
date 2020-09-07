from django.http import JsonResponse
from . import utils
import jwt
import datetime
from ..models import User
import hashlib

KEY = 'key'


def create_user(request):
    ok, missing, data = utils.validate_fields(["username", "password", "fullname"], request)

    if not ok:
        return JsonResponse({'result': 'bad request', 'detail': missing})

    user = User(username=data['username'],
                fullname=data['fullname'],
                hashed_password=hashlib.sha256(data['password']).hexdigest())
    user.save()

    return JsonResponse({'result': 'ok'})


def login(request):
    ok, missing, data = utils.validate_fields(["username", "password"], request)

    if not ok:
        return JsonResponse({'result': 'bad request', 'detail': missing})

    # Validate username and password
    user = {}
    if not User.objects.filter(username=data['username']).exists():
        return JsonResponse({'result': 'badrequest', 'detail': 'User does not exist'})
    else:
        user = User.objects.filter(username=data['username']).first()
        password = hashlib.sha256(data['password']).hexdigest()
        if user.hashed_password != password:
            return JsonResponse({'result': 'bad request', 'detail': 'Password is not correct'})

    data['exp'] = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    access_token = jwt.encode(data, KEY, algorithm='HS256')
    data.pop("exp")
    refresh_token = jwt.encode(data, KEY, algorithm='HS256')

    return JsonResponse({"result": "success", "access_token": access_token, "refresh_token": refresh_token})


def refresh(request):
    ok, missing, data = utils.validate_fields(["refresh_token"], request)

    if not ok:
        return JsonResponse({'result': 'bad request', 'detail': missing})

    data = jwt.decode(data['refresh_token'], KEY, algorithms='HS256')
    data['exp'] = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

    # Validate username and password
    user = {}
    if not User.objects.filter(username=data['username']).exists():
        return JsonResponse({'result': 'badrequest', 'detail': 'User does not exist'})
    else:
        user = User.objects.filter(username=data['username']).first()
        password = hashlib.sha256(data['password']).hexdigest()
        if user.hashed_password != password:
            return JsonResponse({'result': 'bad request', 'detail': 'Password is not correct'})

    key = user.hash_key
    access_token = jwt.encode(data, key, algorithm='HS256')
    data.pop("exp")
    refresh_token = jwt.encode(data, KEY, algorithm='HS256')

    return JsonResponse({"result": "success", "access_token": access_token, "refresh_token": refresh_token})
