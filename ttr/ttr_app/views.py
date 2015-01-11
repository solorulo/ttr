# -*- coding: utf-8 -*-
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from ttr_app.models import *
import json
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def estructura(request):
    return render(request, 'estructura.html')

def login(request):
    
    if request.method == 'GET' or not 'username' in request.POST or not 'password' in request.POST:
        next = request.GET.get('next', None)
        return render(request, 'login.html', {'next':next})
    if not 'username' in request.POST or not 'password' in request.POST:
        return render(request, 'login.html', {'wrong_data':True})
    username = request.POST.get("username", None)
    password = request.POST.get("password", None)
    
    next = request.POST.get('next', None)

    user = authenticate(username=username, password=password)
    try:
        if user is not None and user.is_active:
            auth_login(request, user)
            if next is not None:
                return HttpResponseRedirect(next)
            return HttpResponseRedirect('/estructura')
    except:
        raise PermissionDenied
    return render(request, 'login.html', {'wrong_data':True, 'username':username})

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

   
def newAsignature(request):
    return render(request,'newAsignature.html')
def newUser(request):
    listaAsignaturas=Asignatura.objects.all().values("pk","nombre")
    return render(request,'newUser.html', {"asignaturas": listaAsignaturas})

def registrarUsuario(request):
    if not 'username' in request.POST or not 'password' in request.POST:
        return render(request, 'newUser.html', {'wrong_data':True})
    
    nombreUser = request.POST.get("username", None)
    password = request.POST.get("password", None) 
    nombres = request.POST.get("nombres",None)
    aPaterno = request.POST.get("aPaterno",None)
    aMaterno = request.POST.get("aMaterno", None)
    asignaturas = request.POST.getlist("asignaturas[]", None)
    rol = request.POST.get("rol",None)

    new_user = MyUser(
            username=nombreUser,
            first_name=nombres,
            last_name=aPaterno +" "+ aMaterno,
            password=password,
            rol=int(rol)
        )
    new_user.save()

    asignarAsignatura=Clases(
        user=new_user
    )
    asignarAsignatura.save()

    for asignatura in asignaturas:
        asignarAsignatura.asignaturas.add(int(asignaturas))

    return render(request,'newUser.html')
