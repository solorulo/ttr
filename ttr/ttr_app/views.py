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

def get_estructura_json(node, node_id):
    res = []
    if node == 'base':
        areas = Area.objects.all()
        departamentos = Departamento.objects.all()
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
    elif node == 'departamento':
        # departamento = Departamento.objects.get(pk=int(node_id))
        asignaturas = Asignatura.objects.filter(departamento__pk=int(node_id))
        for asignatura in asignaturas:
            res.append({
                'id' : 'asignatura' + str(asignatura.pk),
                'parent' : '#',
                'text' : asignatura.nombre
                })
    elif node == 'asignatura':
        # asignatura = Asignatura.objects.get(pk=int(node_id))
        clases = Clases.objects.filter(asignaturas__id=int(node_id))
        for clase in clases:
            res.append({
                'id' : 'user' + str(clase.user.pk),
                'parent' : '#',
                'text' : clase.user.get_full_name()
                })

    return res

def estructura_json(request, node, node_id):
	serialized_data = json.dumps(get_estructura_json(node, node_id))
	return HttpResponse(serialized_data, mimetype="application/json")

   
def newAsignature(request):
    listaDepartamentos= Departamento.objects.all().values("pk","nombre")
    listaUsuarios= MyUser.objects.all().values("pk","first_name")
    return render(request,'newAsignature.html',{"departamentos": listaDepartamentos, "usuarios": listaUsuarios})

def registrarAsignatura(request):
    if not 'nombreA' in request.POST:
        return render(request, 'newAsignature.html',{'wrong_data':True})
    nombreAsignatura= request.POST.get("nombreA", None)
    autor= request.POST.get("autorA",None)
    departamento= request.POST.get("departamentoA",None)
    presidente= request.POST.get("presidenteA", None)

    new_asignatura= Asignatura(
            nombre=nombreAsignatura,
            autor_id= int(autor),
            departamento_id= int(departamento),
            presidente_id= int(presidente)
        )
    new_asignatura.save()
    listaDepartamentos= Departamento.objects.all().values("pk","nombre")
    listaUsuarios= MyUser.objects.all().values("pk","first_name")
    return render(request,'newAsignature.html',{"departamentos": listaDepartamentos, "usuarios": listaUsuarios})

def verAsignaturas(request):
    listaAsignaturas= Asignatura.objects.all()
    return render(request,'verAsignaturas.html',{"asignaturas":listaAsignaturas})

def newArea(request):
    
    if request.method == 'POST' and not 'nombreArea' in request.POST:
        return render(request, 'newArea.html',{'wrong_data':True})

    nombreAr= request.POST.get("nombreArea", None)

    new_Area = Area(
            nombre=nombreAr
        )
    new_Area.save()
    return render(request,'newArea.html')
    
def newDepto(request):
    listaAreas= Area.objects.all()
    return render(request, 'newDept.html', {"areas":listaAreas})
def registrarDepto(request):
    if request.method == 'POST' and not 'nombreDepto' in request.POST:
        return render(request, 'newDepto.html', {'wrong_data':True})

    nombreDepartamento = request.POST.get("nombreDepto", None)
    area = request.POST.get("area",None)

    new_Depto= Departamento(
            nombre=nombreDepartamento,
            area_id=int(area)
        )
    new_Depto.save()
    listaAreas= Area.objects.all()
    return render(request, 'newDept.html', {"areas":listaAreas})


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
    asignaturas = request.POST.getlist("asignaturas", None)
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
    print ("asignaturas")
    print ("asignaturas")
    for asignatura in asignaturas:
        print (asignatura)
        asignarAsignatura.asignaturas.add(int(asignatura))
    # asignarAsignatura.asignaturas.save()

    listaAsignaturas=Asignatura.objects.all().values("pk","nombre")
    return render(request,'newUser.html', {"asignaturas": listaAsignaturas})

def visualizarUsuario(request):
    listaUsuarios=MyUser.objects.filter(rol=MyUser.PROFESOR)
    return render(request,"visualizarUsuario.html", {"usuarios": listaUsuarios})

def eliminarUsuario(request):
    id=request.POST.get("id",None)
    deleteUser = MyUser.objects.get(pk=id)
    deleteUser.delete()
    return HttpResponse("true")

def consultarUsuario(request):
    id=request.GET.get("id",None)
    usuario=MyUser.objects.get(pk=id)
    listaAsignaturas=Asignatura.objects.all()
    clases = Clases.objects.get(user_id=id)
    return render(request,"consultarUsuario.html", {"usuario": usuario, "asignaturas": listaAsignaturas, "clases":clases.asignaturas.all()})

def editarUsuario(request):
    return render(request,"consultarUsuario.html")

