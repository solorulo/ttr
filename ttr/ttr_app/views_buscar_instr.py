# -*- coding: utf-8 -*-
from django.db import IntegrityError
from django.db.models import Q, Avg
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
        { "type":"asignatura", "text":"Unidad de aprendizaje"},
        { "type":"docente", "text":"Docente"},
    ]

def buscar(request):
    """
    Unidad de aprendizaje
    Docente
    """
    results = []
    if request.method == "GET":
        type_query = request.GET.get('typeq', '')
        query = request.GET.get('query', '')
        print type_query
        print query
        if (type_query.lower() == 'asignatura'):
            asignaturas_db = Asignatura.objects.all()
            asignaturas_db = asignaturas_db if not query else asignaturas_db.filter(
                Q(nombre__icontains=query) | 
                Q(academia__nombre__icontains=query)
            )
            for asignatura in asignaturas_db:
                results.append({
                    "pk" : asignatura.pk,
                    "nombre" : asignatura.nombre,
                    "url_search" : "./mostrar",
                })
        elif (type_query.lower() == 'docente'):
            users_db = MyUser.objects.all()
            users_db = users_db if not query else users_db.filter(
                Q(rol=MyUser.PROFESOR) | 
                Q(full_name__icontains=query) 
            )
            for user in users_db:
                results.append({
                    "pk" : user.pk,
                    "nombre" : user.get_full_name(),
                    "url_search" : "./mostrar",
                })
        return render(request,'buscar_pre_inst.html', { 
            'TYPESQ': get_types_query(),
            'results' : results, 
            'query' : query, 
            'typeq' : type_query,
        })
    return render(request,'buscar_pre_inst.html', { 
            'TYPESQ': get_types_query(),
        })

def buscar_insts (request):
    if request.method == "GET" :
        type_search = request.GET.get('type', '')
        idx = request.GET.get('id')
        # name = request.GET.get('name')

        instrumentos_db = InstrumentoEvaluacion.objects.all()
        valores_db = EvaluacionInstrumento.objects.all()

        if type_search == 'asignatura':
            instrumentos_db = instrumentos_db.filter(asignatura_id=int(idx))
        elif type_search == 'docente':
            instrumentos_db = instrumentos_db.filter(autor_id=int(idx))
        instrumentos_db = instrumentos_db.annotate(valoracion=Avg('evaluacioninstrumento__valor'))

        return render(request,'buscar_pre_inst.html', {
            # "name" : name,
            "idx" : idx,
            "results" : instrumentos_db,
        })
    return render(request,'buscar_pre_inst.html')


