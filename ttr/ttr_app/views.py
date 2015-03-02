# -*- coding: utf-8 -*-
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from ttr_app.models import *
import json
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def general(request):
    if(request.user.is_authenticated()):
        try:
            id_plantel=request.user.myuser.plantel.pk
            return HttpResponseRedirect("/index")
        except:
             return render(request, 'general.html')
    else:
        return render(request, 'general.html', {'navegacionG':1})
def superior(request):
    listaPlanteles = Plantel.objects.filter(nivel=2)
    return render(request, 'superior.html', {'navegacionG':1, 'listaPlanteles':listaPlanteles})
def mediosuperior(request):
    listaPlanteles = Plantel.objects.get(nivel=1)
    return render(request, 'medioSuperior.html', {'navegacionG':1})

def estructura(request):

    return render(request, 'estructura.html')

def indexInter(request):

    id_plantel=None
    if(request.user.is_authenticated()):
        try:
            id_plantel=request.user.myuser.plantel.pk
        except:
            return HttpResponseRedirect("/login")
    else:
        id_plantel=request.GET.get("id",None)
        plantel= Plantel.objects.get(pk=int(id_plantel))
        request.session["id_plantel"]=int(id_plantel)
        request.session["url"]=plantel.url_logo
        nivel=request.GET.get("niv",None)
        request.session["nivel"]=nivel
        return HttpResponseRedirect("/index/")

def index(request):
    
    id_plantel=None
    if(request.user.is_authenticated()):
        try:
            id_plantel=request.user.myuser.plantel.pk
        except:
            return HttpResponseRedirect("/general/")
    else:
        if(not "id_plantel" in request.session and not request.user.is_authenticated()):
            return HttpResponseRedirect("/general")
        else:
            id_plantel=request.session["id_plantel"]
            print "not auth"
    plantel=Plantel.objects.get(pk=id_plantel)
    request.session["url"]=plantel.url_logo
    mision=plantel.mision
    vision=plantel.vision
    return render(request, 'index.html',{'mision':mision,'vision':vision})

def logout(request):
    id_plantel=request.user.myuser.plantel.pk
    auth_logout(request)
    request.session["id_plantel"]=int(id_plantel)
    # Redirect to a success page.
    return HttpResponseRedirect("/index")

def login(request):


    if(request.user.is_authenticated()):
        try:
            id_plantel=request.user.myuser.plantel.pk
        except:
            pass
    if (request.method == 'GET' or 
        not 'username' in request.POST or 
        not 'password' in request.POST):

        next = request.GET.get('next', None)
        return render(request, 'login.html')
    if not 'username' in request.POST or not 'password' in request.POST:
        return render(request, 'login.html')
    username = request.POST.get("username", None)
    password = request.POST.get("password", None)
    
    next = request.POST.get('next', None)

    user = authenticate(username=username, password=password)
    try:
        if user is not None and user.is_active:
            auth_login(request, user)
            return HttpResponseRedirect("/index")
            if next is not None:
                return HttpResponseRedirect(next)
            return HttpResponseRedirect('/estructura')
        else:
            return render(request, 'login.html', {'error': 'El usuario y/o constraseña no coinciden.' })
    except:
        raise PermissionDenied
    return render(request, 'login.html', {'username':username})

def get_estructura_json(node, node_id):
    res = []
    if node == 'base':
        departamentos = Departamento.objects.all()
        academias = Academia.objects.all()
        for depto in departamentos:
            res.append({
                'id' : 'depto' + str(depto.pk),
                'parent' : '#',
                'text' : depto.nombre
                })
        for academia in academias:
            res.append({
                'id' : 'academia' + str(academia.pk),
                'parent' : 'depto'+str(academia.depto.pk),
                'text' : academia.nombre
                })
    elif node == 'academia':
        asignaturas = Asignatura.objects.filter(academia__pk=int(node_id))
        for asignatura in asignaturas:
            res.append({
                'id' : 'asignatura' + str(asignatura.pk),
                'parent' : '#',
                'text' : asignatura.nombre
                })
    elif node == 'asignatura':
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
    if(not request.user.is_authenticated()):
        return HttpResponseRedirect("/general")
    elif (request.user.myuser.rol == MyUser.PROFESOR):
        return HttpResponseRedirect("/general")
    listaAcademias= Academia.objects.all().values("pk","nombre")
    listaUsuarios= MyUser.objects.all().values("pk","first_name")
    return render(request,'Asignatura/newAsignature.html',{"listaAcademias": listaAcademias, "usuarios": listaUsuarios})

def registrarAsignatura(request):
    if(not request.user.is_authenticated()):
        return HttpResponseRedirect("/general")
    elif (request.user.myuser.rol == MyUser.PROFESOR):
        return HttpResponseRedirect("/general")
    if not 'nombreA' in request.POST:
        return render(request, 'newAsignature.html',{'wrong_data':True})
    nombreAsignatura= request.POST.get("nombreA", None)

    request.user.myuser.pk
    autor= request.user.myuser.pk
    academia= request.POST.get("academiaA",None)
    presidente= request.POST.get("presidenteA", None)

    new_asignatura= Asignatura(
            nombre=nombreAsignatura,
            autor_id= int(autor),
            academia_id= int(academia),
            presidente_id= int(presidente)
        )
    new_asignatura.save()
    listaAcademias= Academia.objects.all().values("pk","nombre")
    listaUsuarios= MyUser.objects.all().values("pk","first_name")
    return render(request,'Asignatura/newAsignature.html',{"listaAcademias": listaAcademias, "usuarios": listaUsuarios})

def verAsignaturas(request):
    if(not request.user.is_authenticated()):
        return HttpResponseRedirect("/general")
    elif (request.user.myuser.rol == MyUser.PROFESOR):
        return HttpResponseRedirect("/general")
    listaAsignaturas= Asignatura.objects.all()
    return render(request,'Asignatura/verAsignaturas.html',{"asignaturas":listaAsignaturas})

def eliminarAsignatura(request):
    if(not request.user.is_authenticated()):
        return HttpResponseRedirect("/general")
    elif (request.user.myuser.rol == MyUser.PROFESOR):
        return HttpResponseRedirect("/general")
    id=request.POST.get("id",None)
    deleteAsignatura = Asignatura.objects.get(pk=id)
    deleteAsignatura.delete()
    return HttpResponse("true")

def consultarAsignatura(request):
    if(not request.user.is_authenticated()):
        return HttpResponseRedirect("/general")
    elif (request.user.myuser.rol == MyUser.PROFESOR):
        return HttpResponseRedirect("/general")

    id=request.GET.get("id",None)
    asignatura=Asignatura.objects.get(pk=id)


    listaAcademias= Academia.objects.all().values("pk","nombre")
    listaUsuarios= MyUser.objects.all().values("pk","first_name")
    return render(request,'Asignatura/consultarAsignatura.html',{"listaAcademias": listaAcademias, "usuarios": listaUsuarios,"asignatura":asignatura})

def editarAsignatura(request):
    if(not request.user.is_authenticated()):
        return HttpResponseRedirect("/general")
    elif (request.user.myuser.rol == MyUser.PROFESOR):
        return HttpResponseRedirect("/general")
    nombreAsignatura = request.POST.get("nombreA", None)
    autor = request.POST.get("autorA", None) 
    academia= request.POST.get("academiaA",None)
    presidente = request.POST.get("presidenteA",None)
    

    id=request.POST.get("id",None)
    asignatura=Asignatura.objects.get(pk=id)

    asignatura.nombre=nombreAsignatura
    asignatura.autor_id=int(autor)
    asignatura.academia_id=int(academia)
    asignatura.presidente_id=int(presidente)

    asignatura.save()
    listaAsignaturas= Asignatura.objects.all()
    return render(request,'Asignatura/verAsignaturas.html',{"asignaturas":listaAsignaturas})

def newDepartamento(request):
    if(not request.user.is_authenticated()):
        return HttpResponseRedirect("/general")
    elif (request.user.myuser.rol == myuser.PROFESOR):
        return HttpResponseRedirect("/general")
    return render(request,'Departamento/newDepartamento.html')

def registrarDepartamento(request):
    if(not request.user.is_authenticated()):
        return HttpResponseRedirect("/general")
    elif (request.user.myuser.rol == MyUser.PROFESOR):
        return HttpResponseRedirect("/general")
    plantel=request.session["id_plantel"]
    nombreDepartamento= request.POST.get("nombreDepartamento", None)

    new_Departamento = Departamento(
            nombre=nombreDepartamento,
            plantel_id=plantel
        )
    new_Departamento.save()
    return render(request,'Departamento/newDepartamento.html')

def verDepartamentos(request):
    if(not request.user.is_authenticated()):
        return HttpResponseRedirect("/general")
    elif (request.user.myuser.rol == MyUser.PROFESOR):
        return HttpResponseRedirect("/general")
    listaDepartamento= Departamento.objects.all()
    return render(request,'Departamento/verDepartamentos.html',{"listaDepartamentos":listaDepartamento})

def eliminarDepartamento(request):
    if(not request.user.is_authenticated()):
        return HttpResponseRedirect("/general")
    elif (request.user.myuser.rol == MyUser.PROFESOR):
        return HttpResponseRedirect("/general")
    id=request.POST.get("id",None)
    deleteDepartamento = Departamento.objects.get(pk=id)
    deleteDepartamento.delete()
    return HttpResponse("true")

def consultarDepartamento(request):
    if(not request.user.is_authenticated()):
        return HttpResponseRedirect("/general")
    elif (request.user.myuser.rol == MyUser.PROFESOR):
        return HttpResponseRedirect("/general")
    id=request.GET.get("id",None)
    depto=Departamento.objects.get(pk=id)
    return render(request,'Departamento/consultarDepartamento.html',{"depto":depto})

def editarDepartamento(request):
    if(not request.user.is_authenticated()):
        return HttpResponseRedirect("/general")
    elif (request.user.myuser.rol == MyUser.PROFESOR):
        return HttpResponseRedirect("/general")
    nombreDepartamento = request.POST.get("nombreA", None)    

    id=request.POST.get("id",None)
    departamento=Departamento.objects.get(pk=id)

    departamento.nombre=nombreDepartamento
    departamento.save()

    listaDepartamentos= Departamento.objects.all()
    return render(request,'Departamento/verDepartamentos.html',{"listaDepartamentos":listaDepartamentos})
    
def newAcademia(request):
    if(not request.user.is_authenticated()):
        return HttpResponseRedirect("/general")
    elif (request.user.myuser.rol == MyUser.PROFESOR):
        return HttpResponseRedirect("/general")
    listaDepartamentos= Departamento.objects.all()
    return render(request, 'Academia/newAcademia.html', {"listaDepartamentos":listaDepartamentos})

def registrarAcademia(request):
    if(not request.user.is_authenticated()):
        return HttpResponseRedirect("/general")
    elif (request.user.myuser.rol ==MyUser.PROFESOR):
        return HttpResponseRedirect("/general")

    nombreAcademia = request.POST.get("nombreAcademia", None)
    departamento = request.POST.get("departamento",None)

    new_Academia= Academia(
            nombre=nombreAcademia,
            depto_id=int(departamento)
        )
    new_Academia.save()
    listaDepartamentos= Departamento.objects.all()
    return render(request, 'Academia/newAcademia.html', {"listaDepartamentos":listaDepartamentos})

def verAcademias(request):
    if(not request.user.is_authenticated()):
        return HttpResponseRedirect("/general")
    elif (request.user.myuser.rol == MyUser.PROFESOR):
        return HttpResponseRedirect("/general")
    listaAcademias= Academia.objects.all()
    return render(request,'Academia/verAcademias.html',{"listaAcademias":listaAcademias})

def eliminarAcademia(request):
    if(not request.user.is_authenticated()):
        return HttpResponseRedirect("/general")
    elif (request.user.myuser.rol == MyUser.PROFESOR):
        return HttpResponseRedirect("/general")
    id=request.POST.get("id",None)
    deleteAcademia = Academia.objects.get(pk=id)
    deleteAcademia.delete()
    return HttpResponse("true")

def consultarAcademia(request):
    if(not request.user.is_authenticated()):
        return HttpResponseRedirect("/general")
    elif (request.user.myuser.rol == myuser.PROFESOR):
        return HttpResponseRedirect("/general")

    id=request.GET.get("id",None)
    academia=Academia.objects.get(pk=id)

    listaDepartamentos= Departamento.objects.all()
    return render(request,'Academia/consultarAcademia.html',{"listaDepartamentos": listaDepartamentos,"academia":academia})

def editarAcademia(request):
    if(not request.user.is_authenticated()):
        return HttpResponseRedirect("/general")
    elif (request.user.myuser.rol == MyUser.PROFESOR):
        return HttpResponseRedirect("/general")
    nombreAcademia = request.POST.get("nombreD", None)
    departamento = request.POST.get("departamentoD",None)
    

    id=request.POST.get("id",None)
    academia=Academia.objects.get(pk=id)

    academia.nombre=nombreAcademia
    academia.depto_id=int(departamento)

    academia.save()
    listaAcademias= Academia.objects.all()
    return render(request,'Academia/verAcademias.html',{"listaAcademias":listaAcademias})

def newUser(request):
    if(not request.user.is_authenticated()):
        return HttpResponseRedirect("/general")
    elif (request.user.myuser.rol == MyUser.PROFESOR):
        return HttpResponseRedirect("/general")
    listaAsignaturas=Asignatura.objects.all().values("pk","nombre")
    return render(request,'Usuario/newUser.html', {"asignaturas": listaAsignaturas})

def registrarUsuario(request):
    if(not request.user.is_authenticated()):
        return HttpResponseRedirect("/general")
    elif (request.user.myuser.rol == MyUser.PROFESOR):
        return HttpResponseRedirect("/general")
    
    nombreUser = request.POST.get("username", None)
    password = request.POST.get("password", None) 
    nombres = request.POST.get("nombres",None)
    aPaterno = request.POST.get("aPaterno",None)
    aMaterno = request.POST.get("aMaterno", None)
    asignaturas = request.POST.getlist("asignaturas", None)
    rol = request.POST.get("rol",None)

    plantel=request.session["id_plantel"]


    new_user = MyUser(
            username=nombreUser,
            first_name=nombres,
            last_name=aPaterno +" "+ aMaterno,
            password=password,
            rol=int(rol),
            plantel_id=int(plantel),
        )
    new_user.save()

    asignarAsignatura=Clases(
        user=new_user
    )
    asignarAsignatura.save()
    for asignatura in asignaturas:
        asignarAsignatura.asignaturas.add(int(asignatura))
    # asignarAsignatura.asignaturas.save()

    listaAsignaturas=Asignatura.objects.all().values("pk","nombre")
    return render(request,'Usuario/newUser.html', {"asignaturas": listaAsignaturas, "mensaje": "Usuario Registrado"})

def visualizarUsuario(request):
    if(not request.user.is_authenticated()):
        return HttpResponseRedirect("/general")
    elif (request.user.myuser.rol == MyUser.PROFESOR):
        return HttpResponseRedirect("/general")
    listaUsuarios=MyUser.objects.filter(rol=MyUser.PROFESOR)
    return render(request,"Usuario/visualizarUsuario.html", {"usuarios": listaUsuarios})

def eliminarUsuario(request):
    if(not request.user.is_authenticated()):
        return HttpResponseRedirect("/general")
    elif (request.user.myuser.rol == MyUser.PROFESOR):
        return HttpResponseRedirect("/general")
    id=request.POST.get("id",None)
    deleteUser = MyUser.objects.get(pk=id)
    deleteUser.delete()
    return HttpResponse("true")

def consultarUsuario(request):
    if(not request.user.is_authenticated()):
        return HttpResponseRedirect("/general")
    elif (request.user.myuser.rol == MyUser.PROFESOR):
        return HttpResponseRedirect("/general")
    id=request.GET.get("id",None)
    usuario=MyUser.objects.get(pk=id)
    listaAsignaturas=Asignatura.objects.all()
    clases = Clases.objects.get(user_id=id)
    return render(request,"Usuario/consultarUsuario.html", {"usuario": usuario, "asignaturas": listaAsignaturas, "clases":clases.asignaturas.all()})

def editarUsuario(request):
    if(not request.user.is_authenticated()):
        return HttpResponseRedirect("/general")
    elif (request.user.myuser.rol ==MyUser.PROFESOR):
        return HttpResponseRedirect("/general")
    
    nombreUser = request.POST.get("username", None)
    password = request.POST.get("password", None) 
    nombres = request.POST.get("nombres",None)
    apellidos = request.POST.get("apellidos",None)
    asignaturas = request.POST.getlist("asignaturas", None)
    rol = request.POST.get("rol",None)    

    id=request.POST.get("id",None)
    usuario=MyUser.objects.get(pk=id)

    usuario.username=nombreUser
    usuario.first_name=nombres
    usuario.last_name=apellidos
    usuario.password=password
    usuario.rol=int(rol)

    usuario.save()

    asignarAsignatura=Clases.objects.get(user_id=id)
    asignarAsignatura.asignaturas.clear()
    for asignatura in asignaturas:
        asignarAsignatura.asignaturas.add(int(asignatura))

    listaUsuarios=MyUser.objects.filter(rol=MyUser.PROFESOR)
    return render(request,"Usuario/visualizarUsuario.html", {"usuarios": listaUsuarios})
