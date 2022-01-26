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
        { "type":"instrumento", "text":"Instrumento"},
    ]

def get_types_order():
    return [
        { "type":"no", "text":"--"},
        { "type":"asc", "text":"Ascendente"},
        { "type":"dsc", "text":"Descendente"},
    ]

def buscar(request):
    """
    Unidad de aprendizaje
    Docente
    Instrumentos
    """
    results = []
    if request.method == "GET":
        type_query = request.GET.get('typeq', '')
        query = request.GET.get('query', '')
        print (type_query)
        print (query)
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
        elif (type_query.lower() == 'instrumento'):
            return HttpResponseRedirect("./mostrar?type=instrumento&query=" + query)
            # instrumentos_db = InstrumentoEvaluacion.objects.all()
            # instrumentos_db = instrumentos_db.filter(titulo__icontains=query).annotate(valoracion=Avg('evaluacioninstrumento__valor'))
            # for inst in instrumentos_db:
            #     type_inst = ''
            #     stype_inst = ''
            #     try:
            #         if inst.rubrica:
            #             type_inst = 'Rúbrica'
            #             stype_inst = 'rubrica'
            #     except:
            #         pass
            #     try:
            #         if inst.listacotejo:
            #             type_inst = 'Lista de cotejo'
            #             stype_inst = 'listacotejo'
            #     except:
            #         pass
            #     try:
            #         if inst.listaobservacion:
            #             type_inst = 'Guía de observación'
            #             stype_inst = 'listaobs'
            #     except:
            #         pass
                
                
            #     results.append({
            #         "pk" : inst.pk,
            #         "nombre" : inst.titulo,
            #         "type" : type_inst,
            #         "stype" : stype_inst,
            #         "valoracion" : inst.valoracion,
            #         "url_search" : "/instrumento",
            #     })
        return render(request,'buscar_pre_inst.html', { 
            'TYPESQ': get_types_query(),
            'results' : results, 
            'query' : query, 
            'typeq' : type_query,
        })
    return render(request,'buscar_pre_inst.html', { 
            'TYPESQ': get_types_query(),
        })

def get_types_inst():
    return [
        { "type":"no", "text":"--"},
        { "type":"rubrica", "text":"Rúbrica"},
        { "type":"listacotejo", "text":"Lista de Cotejo"},
        { "type":"listaobservacion", "text":"Guíe de observación"},
    ]

def buscar_insts (request):
    if request.method == "GET" :
        type_search = request.GET.get('type', '')
        type_inst = request.GET.get('type_inst', '')
        idx = request.GET.get('id')
        name = request.GET.get('query')
        oficial = request.GET.get('oficial', '')
        order = request.GET.get('order')
        level_show = request.GET.get('level_show', InstrumentoEvaluacion.PLANTEL)

        instrumentos_db = None
        if not type_inst:
            instrumentos_db = InstrumentoEvaluacion.objects.all()
        elif type_inst == 'rubrica':
            instrumentos_db = Rubrica.objects.all()
        elif type_inst == 'listacotejo':
            instrumentos_db = ListaCotejo.objects.all()
        elif type_inst == 'listaobservacion':
            instrumentos_db = ListaObservacion.objects.all()
        else:
            instrumentos_db = InstrumentoEvaluacion.objects.all()

        if type_search == 'asignatura':
            instrumentos_db = instrumentos_db.filter(asignatura_id=int(idx))
            objectx = Asignatura.objects.get(pk=int(idx))
            name = objectx.nombre
        elif type_search == 'docente':
            instrumentos_db = instrumentos_db.filter(autor_id=int(idx))
            objectx = MyUser.objects.get(pk=int(idx))
            name = objectx.get_full_name()
        elif type_search == 'instrumento':
            instrumentos_db = instrumentos_db.filter(titulo__icontains=name).annotate(valoracion=Avg('evaluacioninstrumento__valor'))

        if oficial.lower() == 'true':
            instrumentos_db = instrumentos_db.filter(oficial=True)

        if order == 'asc':
            instrumentos_db = instrumentos_db.order_by('titulo')
        elif order == 'dsc':
            instrumentos_db = instrumentos_db.order_by('-titulo')

        instrumentos_db.filter(level_show__gte=int(level_show))

        instrumentos_db = instrumentos_db.annotate(valoracion=Avg('evaluacioninstrumento__valor'))

        return render(request,'buscar_inst.html', {
            # "name" : name,
            "idx" : idx,
            "type_search" : type_search,
            "type_inst" : type_inst,
            "results" : instrumentos_db,
            "name" : name,
            "oficial" : oficial,
            "order" : order,
            "level_show" : level_show,
            "url_inst" : '/instrumento',
            'TYPESORDER': get_types_order(),
            'TYPESINST': get_types_inst(),
            'TYPESSHOW': InstrumentoEvaluacion.TIPO_CHOICES,
        })
    return render(request,'buscar_inst.html')


