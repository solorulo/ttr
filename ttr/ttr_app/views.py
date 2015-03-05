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
def portal(request):
    listaPlantelesSUP = Plantel.objects.filter(nivel=2)
    listaPlantelesMED = Plantel.objects.filter(nivel=1)

    if(request.user.is_authenticated()):
        try:
            id_plantel=request.user.myuser.plantel.pk
            return HttpResponseRedirect("/index")
        except:
            listaPlantelesSUP = Plantel.objects.filter(nivel=2)
            listaPlantelesMED = Plantel.objects.filter(nivel=1)
            return render(request, 'portal.html',{'listaPlantelesSUP':listaPlantelesSUP,'listaPlantelesMED':listaPlantelesMED})
    else:
        return render(request, 'portal.html',{'listaPlantelesSUP':listaPlantelesSUP,'listaPlantelesMED':listaPlantelesMED})

def general(request):
    if(request.user.is_authenticated()):
        try:
            id_plantel=request.user.myuser.plantel.pk
            return HttpResponseRedirect("/index")
        except:
             return render(request, 'portal.html')
    else:
        return render(request, 'portal.html', {'navegacionG':1})
def superior(request):
    listaPlanteles = Plantel.objects.filter(nivel=2)
    return render(request, 'superior.html', {'navegacionG':1, 'listaPlanteles':listaPlanteles})
def mediosuperior(request):
    listaPlanteles = Plantel.objects.get(nivel=1)
    return render(request, 'medioSuperior.html', {'navegacionG':1})

def estructura(request):
    listaDocentes= MyUser.objects.filter(rol=MyUser.PROFESOR).values("pk","full_name")
    return render(request, 'estructura.html',{'docentes':listaDocentes})

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
            return HttpResponseRedirect("/portal/")
    else:
        if(not "id_plantel" in request.session and not request.user.is_authenticated()):
            return HttpResponseRedirect("/portal")
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
            return render(request, 'login.html', {'error': 'El usuario y/o contraseña no coinciden.' })
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
                'text' : depto.nombre,
                'icon': "/static/img/iconos/departamento.png"
                })
        for academia in academias:
            res.append({
                'id' : 'academia' + str(academia.pk),
                'parent' : 'depto'+str(academia.depto.pk),
                'text' : academia.nombre,
                'icon': "/static/img/iconos/academia.png"
                })
    elif node == 'academia':
        asignaturas = Asignatura.objects.filter(academia__pk=int(node_id))
        for asignatura in asignaturas:
            res.append({
                'id' : 'asignatura' + str(asignatura.pk),
                'parent' : '#',
                'text' : asignatura.nombre,
                'icon': "/static/img/iconos/asignatura.png"
                })
    elif node == 'asignatura':
        clases = Clases.objects.filter(asignaturas__id=int(node_id))
        for clase in clases:
            res.append({
                'id' : 'user' + str(clase.user.pk),
                'parent' : '#',
                'text' : clase.user.get_full_name(),
                'icon': "/static/img/iconos/docente.png"
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

def agregarDocente(request):
    if(not request.user.is_authenticated()):
        return HttpResponseRedirect("/general")
    elif (request.user.myuser.rol == MyUser.ADMINISTRADOR):
        docentes = request.POST.getlist("docentes", None)
        idAsignatura= request.POST.get("asignatura",None)

        for docente in docentes:
            asignarAsignatura, created=Clases.objects.get_or_create(user_id=docente
            )
            asignarAsignatura.asignaturas.add(int(idAsignatura))
    
    return HttpResponseRedirect("/estructura/")

def quitarDocente(request):
    if(not request.user.is_authenticated()):
        return HttpResponseRedirect("/general")
    elif (request.user.myuser.rol == MyUser.ADMINISTRADOR):
        idDocente = request.POST.get("docente", None)
        idAsignatura= request.POST.get("asignatura",None)

        quitarAsignatura=Clases.objects.get(user_id=idDocente)
        quitarAsignatura.asignaturas.remove(int(idAsignatura))

    return HttpResponseRedirect("/estructura/")



def newDepartamento(request):
    if(not request.user.is_authenticated()):
        return HttpResponseRedirect("/general")
    elif (request.user.myuser.rol == MyUser.PROFESOR):
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
    elif (request.user.myuser.rol == MyUser.PROFESOR):
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
    return HttpResponseRedirect("/estructura")

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
    aPaterno = request.POST.get("aPaterno",'')
    aMaterno = request.POST.get("aMaterno", '')
    asignaturas = request.POST.getlist("asignaturas", None)
    rol = request.POST.get("rol",None)

    plantel=request.user.myuser.plantel


    new_user = MyUser(
            username=nombreUser,
            first_name=nombres,
            last_name=aPaterno +" "+ aMaterno,
            rol=int(rol),
            plantel=plantel,
        )
    try:
        new_user.save()

        asignarAsignatura=Clases(
            user=new_user
        )
        asignarAsignatura.save()
        for asignatura in asignaturas:
            asignarAsignatura.asignaturas.add(int(asignatura))
        # asignarAsignatura.asignaturas.save()

        listaAsignaturas=Asignatura.objects.all().values("pk","nombre")
        return render(request,'Usuario/newUser.html', {"asignaturas": listaAsignaturas ,"mensaje": "1" })
            
    except:
        listaAsignaturas=Asignatura.objects.all().values("pk","nombre")   
        return render(request,'Usuario/newUser.html', {"asignaturas": listaAsignaturas, "mensaje": "2", "username":nombreUser})
    

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
    clases = None
    asignaturas = None
    if usuario.rol == MyUser.PROFESOR:
        clases = Clases.objects.get(user_id=id)
        asignaturas = clases.asignaturas.all()

    return render(request,"Usuario/consultarUsuario.html", {"usuario": usuario, "asignaturas": listaAsignaturas, "clases":asignaturas})

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

    id=request.POST.get("id",None)
    usuario=MyUser.objects.get(pk=id)

    usuario.username=nombreUser
    usuario.first_name=nombres
    usuario.last_name=apellidos
    usuario.set_password(password)

    usuario.save()

    asignarAsignatura=Clases.objects.get(user_id=id)
    asignarAsignatura.asignaturas.clear()
    for asignatura in asignaturas:
        asignarAsignatura.asignaturas.add(int(asignatura))

    listaUsuarios=MyUser.objects.filter(rol=MyUser.PROFESOR)
    return HttpResponseRedirect("/buscar")


def miperfil(request):
    if(not request.user.is_authenticated() or request.user.myuser.rol==MyUser.ADMINISTRADOR):
        return HttpResponseRedirect("/portal")
    else: 
        try:
            id_user=request.user.myuser.pk
        except:
            return HttpResponseRedirect("/portal")

    listaInstrumentos=InstrumentoEvaluacion.objects.filter(autor=id_user)
    listaUnidades=None
    unidadJefe= None

    try:
        listaUnidades= Clases.objects.get(user_id=id_user).asignaturas.all()
        unidadJefe= Asignatura.objects.get(presidente_id=id_user)
    except:
        unidadJefe="No es jefe de alguna Unidad de Aprendizaje"
    print listaInstrumentos
    return render(request, 'Usuario/perfil.html',{"instrumentos":listaInstrumentos, "unidades":listaUnidades, "jefe":unidadJefe})

def cambiarPrivacidad(request):
    
    id=request.POST.get("id",None)
    if not id:
        mensaje="No existe este instrumento de evaluación"
        respuesta={
        "mensaje": mensaje,
        "estatus": False,
        }
        return HttpResponse (json.dumps(respuesta), mimetype='application/json')

    privacidad = request.POST.get("privacidad", None)

    try:
        instrumento=InstrumentoEvaluacion.objects.get(pk=id)
    except:
        mensaje="Este instrumento no existe en la base de datos"
        respuesta={
        "mensaje": mensaje,
        "estatus": True,
        }
        return HttpResponse (json.dumps(respuesta), mimetype='application/json')


    instrumento.level_show=int(privacidad)
    try:
        instrumento.save()
        mensaje="Se ha cambiado el nivel de privacidad del instrumento de evaluación"
    except:
        mensaje="No se puede cambiar el tipo de privacidad"


    respuesta={
        "mensaje": mensaje,
        "estatus": True,
    }
    return HttpResponse (json.dumps(respuesta), mimetype='application/json')

