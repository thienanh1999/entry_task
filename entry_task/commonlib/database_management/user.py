from commonlib.models import User
from . import utils
import hashlib
import time


class UserManagement():

    def retrieve(self, username):
        return utils.get_object_or_none(User, username=username)
    
    def create(self, username, password, fullname):
        hash_key = utils.get_random_string(8)
    
        user = User.objects.create(username=username,
                                   fullname=fullname,
                                   hashed_password=hashlib.sha256(
                                       hashlib.sha256(password).hexdigest() + hash_key).hexdigest(),
                                   salt=hash_key,
                                   is_admin=0,
                                   created_at=int(time.time()))
        return user.as_dict()
