from .base import validate_fields, get_validator_object
from .base import STRING, INT, UNSIGNED_INT


def create_event(request):
	validator = [
		get_validator_object('title', STRING, True),
		get_validator_object('description', STRING, False),
		get_validator_object('location', STRING, True),
		get_validator_object('images', STRING, False),
		get_validator_object('start', UNSIGNED_INT, True),
		get_validator_object('end', UNSIGNED_INT, True),
		get_validator_object('category', STRING, False),
	]
	return validate_fields(request.POST, validator)
