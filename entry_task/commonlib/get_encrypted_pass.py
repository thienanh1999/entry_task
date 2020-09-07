import hashlib


def get_encrypted_pass(raw_pass, salt, verify_code):
	key = hashlib.sha256(raw_pass).hexdigest()
	key = hashlib.sha256(key + salt).hexdigest()
	key = hashlib.sha256(key + verify_code).hexdigest()
	
	return key


if __name__ == '__main__':
	print get_encrypted_pass('1', 'tcvymaww', 'gcpcbvuvoqyqumrwrwbudgjfoervrkkolqnsrsajjazfofegiy')
