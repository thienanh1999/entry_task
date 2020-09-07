import jwt
from ..models import User
import hashlib
from django.http import JsonResponse


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
        user = User.objects.filter(username=username).first()
        password = hashlib.sha256(password).hexdigest()
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
