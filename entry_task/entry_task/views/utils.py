import jwt
from commonlib.models import User
import hashlib
from django.http import JsonResponse
import random
import string
import os
import datetime


KEY = os.environ.get('JWT_KEY', 'key')


def validate_fields(fields, request):
    ok = True
    missing = []
    data = request.POST
    response = {}
    for field in fields:
        value = data.get(field, None)
        if value is None:
            ok = False
            missing.append(field)
        else:
            response[field] = value

    missing = ','.join(missing)
    missing = 'Missing fields: ' + missing
    return ok, missing, response


def validate_access_token(token):
    """
    :param token: string - access token
    :return: username (if valid) or None
    """
    try:
        decoded = jwt.decode(token, KEY, leeway=datetime.timedelta(hours=1), algorithms='HS256')
    except Exception:
        decoded = False

    if not decoded:
        return None
    
    username = decoded.get('username', None)
    if username is None:
        return None
    else:
        return username


def validate_token(token, key, expired_time):
    try:
        decoded = jwt.decode(token, key, leeway=expired_time, algorithms='HS256')
    except Exception:
        decoded = False
    return decoded


def check_user(username, password):
    if not User.objects.filter(username=username).exists():
        return False
    else:
        user = get_object_or_none(User, username=username)
        password = hashlib.sha256(password + user.hash_key).hexdigest()
        if user.hashed_password != password:
            return False
    return True


def response_200(detail):
    return JsonResponse({
        'result': 'success',
        'detail': detail
    })


def response_400(detail=None):
    if detail is None:
        return JsonResponse({'result': 'bad request'})
    else:
        return JsonResponse({
            'result': 'bad request',
            'detail': detail
        })


def response_404(detail=None):
    if detail is None:
        return JsonResponse({'result': 'not found'})
    else:
        return JsonResponse({
            'result': 'not found',
            'detail': detail
        })


def response_403(detail=None):
    if detail is None:
        return JsonResponse({'result': 'forbidden'})
    else:
        return JsonResponse({
            'result': 'forbidden',
            'detail': detail
        })


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def get_object_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None
