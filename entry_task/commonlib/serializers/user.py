from .base import validate_fields, get_validator_object
from .base import STRING, INT, UNSIGNED_INT


def create_user(request):
	"""
	:param request:
	:return: data or None
	"""
	validator = [
		get_validator_object('username', STRING, True),
		get_validator_object('password', STRING, True),
		get_validator_object('fullname', STRING, True)
	]
	return validate_fields(request.POST, validator)


def get_salt(request):
	validator = [
		get_validator_object('username', STRING, True)
	]
	return validate_fields(request.POST, validator)


def get_access_token(request):
	validator = [
		get_validator_object('username', STRING, True),
		get_validator_object('encrypted_password', STRING, True)
	]
	return validate_fields(request.POST, validator)
