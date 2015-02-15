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
        if (type_query.lower() == 'departamento'):
            deptos_db = Departamento.objects.all()
            deptos_db = deptos_db if query else deptos_db.filter(nombre__iexact=query)
            for obj in deptos_db:
                results.append({
                    "pk" : obj.pk,
                    "name" : obj.nombre,
                    "url-see" : "/departamento/consultar/",
                    "url-delete" : "/departamento/borrar/",
                })
        elif (type_query.lower() == 'academia'):
            academias_db = Academia.objects.all()
            academias_db = academias_db if query else academias_db.filter(nombre__iexact=query)
            for obj in academias_db:
                results.append({
                    "pk" : obj.pk,
                    "name" : obj.nombre,
                    "url-see" : "/academia/consultar/",
                    "url-delete" : "/academia/borrar/",
                })
        elif (type_query.lower() == 'asignatura'):
            asignaturas_db = Asignatura.objects.all()
            asignaturas_db = asignaturas_db if asignaturas_db else asignaturas_db.filter(nombre__iexact=query)
            for obj in asignaturas_db:
                results.append({
                    "pk" : obj.pk,
                    "name" : obj.nombre,
                    "url-see" : "/asignatura/consultar/",
                    "url-delete" : "/asignatura/borrar/",
                })
        elif (type_query.lower() == 'usuario'):
            users_db = MyUser.objects.all()
            users_db = users_db if query else users_db.filter(nombre__iexact=query)
            for obj in asignaturas_db:
                results.append({
                    "pk" : obj.pk,
                    "name" : obj.get_full_name(),
                    "url-see" : "/usuario/consultar/",
                    "url-delete" : "/usuario/borrar/",
                })
        return render(request,'buscar.html', { 'results' : results })
    return render(request,'buscar.html')
