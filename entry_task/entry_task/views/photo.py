import datetime
from . import utils
from django.core.files.storage import FileSystemStorage
from commonlib.database_management.user import UserManagement
import os

KEY = os.environ.get('JWT_KEY', 'key')
HOST = 'localhost:8000/media'


def upload(request):
    token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
    user_data = utils.validate_token(token, KEY, datetime.timedelta(hours=1))
    if user_data:
        if not utils.check_user(user_data['username'], user_data['password']):
            return utils.response_400('Invalid access token')
    else:
        return utils.response_400('Invalid access token')

    # Get user_id
    user = UserManagement().retrieve(username=user_data['username'])
    user_id = user.id

    fs = FileSystemStorage()
    response = []

    images = request.FILES.getlist('image')
    for image in images:
        image_name = image.name
        image_path = "user_%s/%s" % (user_id, image_name)
        path = fs.save(image_path, image)
        response.append("%s/%s" % (HOST, path))

    return utils.response_200(response)
