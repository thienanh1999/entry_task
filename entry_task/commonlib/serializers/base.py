STRING = 0
INT = 1
UNSIGNED_INT = 2


def validate_fields(data, validator):
	"""
	[
		{
			"key": <string>,
			"type": <int>,
			"required": <bool>,
		}
	]
	:param data:
	:param validator:
	:return:
	"""
	for field in validator:
		key = field['key']
		type = field['type']
		required = field['required']
		value = data.get(key, None)
		if value is None and required is True:
			return False
		else:
			if not check_type(value, type):
				return False
	
	return True
		
		
def check_type(var, type):
	if type == STRING:
		try:
			var = str(var)
			return isinstance(var, str)
		except:
			return False
	if type == INT:
		try:
			var = int(var)
			return isinstance(var, int)
		except:
			return False
	if type == UNSIGNED_INT:
		try:
			var = int(var)
			x = isinstance(var, int)
			if not x or x < 0:
				return False
			else:
				return True
		except:
			return False


def get_validator_object(key, type, required):
	return {
		'key': key,
		'type': type,
		'required': required,
	}
