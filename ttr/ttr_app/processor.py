from ttr_app.models import MyUser

def roles(request):
	ROLES_VALUES = {}
	for key, value in MyUser.TIPO_CHOICES:
		ROLES_VALUES[value.upper()] = key
	return {
		'ROLES_CHOICES': MyUser.TIPO_CHOICES, 
		'ROLES' : ROLES_VALUES,
	}