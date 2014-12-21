# -*- coding: utf-8 -*-
from django.db import IntegrityError
from django.shortcuts import render
from ttr_app.models import *
import json
from django.http import HttpResponse

# Create your views here.
def estructura(request):
	return render(request, 'estructura.html')

def login(request):
    return render(request, 'login.html')
def index(request):
    return render(request, 'index.html')

def get_estructura_json():
	areas = Area.objects.all()
	departamentos = Departamento.objects.all()
	res = []
	for area in areas:
		res.append({
			'id' : 'area' + str(area.pk),
			'parent' : '#',
			'text' : area.nombre
			})
	for dep in departamentos:
		res.append({
			'id' : 'depto' + str(dep.pk),
			'parent' : 'area'+str(dep.area.pk),
			'text' : dep.nombre
			})
	return res

def estructura_json(request):
	serialized_data = json.dumps(get_estructura_json())
	return HttpResponse(serialized_data, mimetype="application/json")

def newUser(request):
	return render(request,'newUser.html')	
