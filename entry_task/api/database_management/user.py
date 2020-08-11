from  ..models import User
from . import utils


class UserManagement():

    def retrieve(self, username):
        return utils.get_object_or_none(User, username=username)
