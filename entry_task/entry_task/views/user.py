from django.http import JsonResponse

from . import utils
import jwt
import datetime
import hashlib
import os

from commonlib.database_management.user import UserManagement
from commonlib.models import User
from commonlib.serializers import user as user_validator

KEY = os.environ.get('JWT_KEY', 'key')


def create_user(request):
    if not user_validator.create_user(request):
        return utils.response_400()
    
    data = request.POST
    
    # Check if user exist
    if utils.get_object_or_none(User, username=data['username']) is not None:
        return utils.response_400('username already exists.')

    user = UserManagement().create(data['username'], data['password'], data['fullname'])

    return utils.response_200(user)


def get_salt(request):
    if not user_validator.get_salt(request):
        return utils.response_400()
    
    data = request.POST
    
    # Check if user exists
    user = utils.get_object_or_none(User, username=data['username'])
    if user is None:
        return utils.response_404('User does not exist.')
    
    verify_code = utils.get_random_string(50)
    salt = user.salt
    User.objects.filter(id=user.id).update(verify_code=verify_code)
    
    return utils.response_200({
        'salt': salt,
        'verify_code': verify_code,
    })


def login(request):
    if not user_validator.get_access_token(request):
        return utils.response_400()
    
    data = {}
    data['username'] = request.POST['username']
    data['encrypted_password'] = request.POST['encrypted_password']

    # Validate username and password
    user = utils.get_object_or_none(User, username=data['username'])
    if user is None:
        return utils.response_404('User does not exist')
    else:
        if user.verify_code is None:
            return utils.response_400('Wrong password')
        else:
            correct_enc_pass = hashlib.sha256(user.hashed_password + user.verify_code).hexdigest()
            User.objects.filter(id=user.id).update(verify_code=None)
            if correct_enc_pass != data['encrypted_password']:
                return utils.response_400('Wrong password')

    data['exp'] = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    access_token = jwt.encode(data, KEY, algorithm='HS256')

    return JsonResponse({"result": "success", "access_token": access_token})
