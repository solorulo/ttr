from ttr_app.models import MyUser, InstrumentoEvaluacion

def roles(request):
	ROLES_VALUES = {}
	for key, value in MyUser.TIPO_CHOICES:
		ROLES_VALUES[value.upper()] = key

	PRIVACIDAD_VALUES={}
	for key, value in InstrumentoEvaluacion.TIPO_CHOICES:
		PRIVACIDAD_VALUES[value.upper()]=key

	return {
		'ROLES_CHOICES': MyUser.TIPO_CHOICES, 
		'ROLES' : ROLES_VALUES,

		'PRIVACIDAD_CHOICES': InstrumentoEvaluacion.TIPO_CHOICES,
		'PRIVACIDAD': PRIVACIDAD_VALUES,
	}