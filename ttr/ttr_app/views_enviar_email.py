from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from ttr_app.models import *
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail.message import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings


def enviar_correo(request):
	correo=request.POST.get("email",None)
	Usuario=MyUser.objects.get(username=correo)
	print "correo:"+ correo
	if Usuario is not None:
		email_context={
			'Recuperar Contrasena',
			Usuario.get_full_name(),
			Usuario.username,
			Usuario.password
		}
		
		subject='Recuperar contrasena'
		text_content = Usuario.password
		from_email= settings.EMAIL_HOST_USER
		to='deivid.091291@gmail.com'

		msg=EmailMultiAlternatives(subject,text_content,from_email,[to])

		#se envia el correo
		msg.send()
	
	return HttpResponseRedirect('/')
