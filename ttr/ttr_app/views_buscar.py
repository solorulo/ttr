# -*- coding: utf-8 -*-
from django.db import IntegrityError
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from ttr_app.models import *
import json
from django.http import HttpResponse, HttpResponseRedirect

def get_types_query():
    return [
        { "type":"departamento", "text":"Departamento"},
        { "type":"academia", "text":"Academia"},
        { "type":"asignatura", "text":"Unidad de aprendizaje"},
        { "type":"usuario", "text":"Usuarios"},
    ]

def buscar(request):
    """
    Departamento
    Academia
    Unidad de aprendizaje
    Usuario
    """
    results = []
    if request.method == "GET":
        type_query = request.GET.get('typeq', '')
        query = request.GET.get('query', '')
        print type_query
        print query
        if (type_query.lower() == 'departamento'):
            deptos_db = Departamento.objects.all()
            deptos_db = deptos_db if not query else deptos_db.filter(nombre__icontains=query)
            """
            Q(nombre__icontains=query) | 
            Q(subtitle__icontains=q) | 
            Q(content__icontains=q)
            """
            for obj in deptos_db:
                results.append({
                    "pk" : obj.pk,
                    "name" : obj.nombre,
                    "url_modif" : "/departamento/consultar/",
                    "url_delete" : "/departamento/borrar/",
                })
        elif (type_query.lower() == 'academia'):
            academias_db = Academia.objects.all()
            academias_db = academias_db if not query else academias_db.filter(nombre__icontains=query)
            for obj in academias_db:
                results.append({
                    "pk" : obj.pk,
                    "name" : obj.nombre,
                    "url_modif" : "/academia/consultar/",
                    "url_delete" : "/academia/borrar/",
                })
        elif (type_query.lower() == 'asignatura'):
            asignaturas_db = Asignatura.objects.all()
            asignaturas_db = asignaturas_db if not query else asignaturas_db.filter(nombre__icontains=query)
            for obj in asignaturas_db:
                results.append({
                    "pk" : obj.pk,
                    "name" : obj.nombre,
                    "url_modif" : "/asignatura/consultar/",
                    "url_delete" : "/asignatura/borrar/",
                })
        elif (type_query.lower() == 'usuario'):
            users_db = MyUser.objects.all()
            users_db = users_db if not query else users_db.filter(full_name__icontains=query)
            for obj in users_db:
                results.append({
                    "pk" : obj.pk,
                    "name" : obj.get_full_name(),
                    "rol": obj.get_rol_display(),
                    "url_modif" : "/usuario/consultar/",
                    "url_delete" : "/usuario/borrar/",
                })
        return render(request,'buscar.html', { 
            'TYPESQ': get_types_query(),
            'results' : results, 
            'query' : query, 
            'typeq' : type_query 
        })
    return render(request,'buscar.html')
