# -*- coding: utf-8 -*-
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from ttr_app.models import *
import json
from django.http import HttpResponse, HttpResponseRedirect

def agregar(request):
    if request.method == "POST":
        titulo = request.POST.get('titulo')
        autor = request.POST.get('autor')
        asignatura = request.POST.get('asignatura')
        oficial = request.POST.get('oficial')

        print request.POST

        listaobs = request.POST.get('listaobs[]')
        print "listaobs "
        listaobs = json.loads(listaobs)
        print listaobs

        try:
            autor = request.user.myuser.pk
        except:
            pass

        new_listaobs = ListaObservacion(
            titulo=titulo,
            autor_id=int(autor),
            asignatura_id=int(asignatura),
            oficial=(oficial.lower()=="true"),
        )
        new_listaobs.save()

        for idx, indicador in enumerate(listaobs):
            print "nuevo indicador"
            print indicador
            """
            'text' : text,
            'value' : value,
            'index' : meta_index
            """
            ind_text = indicador['text']
            ind_value = indicador['value']
            new_indicador = IndicadorListaObs(
                listaobs_id=new_listaobs.pk,
                texto=ind_text,
                valor=ind_value
            )
            new_indicador.save()
        
        return HttpResponse('true')
    return render(request,'Instrumento/Observacion/obs_agregar.html', 
        {
            "ind_choices" : IndicadorListaObs.TIPO_CHOICES,
            "ASIGNATURAS" : Asignatura.objects.all(),
        })

def ver(request):
    idx = request.GET.get('id')
    the_obs = get_object_or_404(ListaObservacion, pk=int(idx))
    the_indicadores = IndicadorListaObs.objects.filter(listaobs_id=the_obs.pk)
    print the_indicadores
    return render(request,'Instrumento/Observacion/obs_ver.html', { 
        'instrumento':the_obs, 
        'indicadores' : the_indicadores, 
    })

def editar(request):
    idx = request.GET.get('id')
    if request.method == "POST":
        titulo = request.POST.get('titulo')
        autor = request.POST.get('autor')
        asignatura = request.POST.get('asignatura')
        oficial = request.POST.get('oficial')

        print request.POST

        listaobs = request.POST.get('listaobs[]')
        print "listaobs "
        listaobs = json.loads(listaobs)
        print listaobs

        new_listaobs = None
        try:
            autor = request.user.myuser.pk
            new_listaobs = get_object_or_404(ListaObservacion,
                pk=int(idx),
                autor_id=autor,
            )
        except:
            return HttpResponse('false')



        new_listaobs.titulo=titulo
        new_listaobs.asignatura_id = int(asignatura)
        new_listaobs.oficial=(oficial.lower()=="true")
        new_listaobs.save()

        IndicadorListaObs.objects.filter(listaobs_id=new_listaobs.pk).delete()
        for idx, indicador in enumerate(listaobs):
            print "nuevo indicador"
            print indicador
            """
            'text' : text,
            'value' : value,
            'index' : meta_index
            """
            ind_text = indicador['text']
            print "ind_text "+ind_text
            ind_value = indicador['value']
            print "ind_value "+ind_value
            ind_index = None if not 'index' in indicador else indicador['index']
            print "ind_index "+ind_index
            new_indicador = IndicadorListaObs(
                listaobs_id=new_listaobs.pk,
                texto=ind_text,
                valor=ind_value
            )
            new_indicador.save()
        return HttpResponse('true')
    elif request.method == 'GET':
        the_obs = get_object_or_404(ListaObservacion, pk=int(idx))
        the_indicadores = IndicadorListaObs.objects.filter(listaobs_id=the_obs.pk)
        print the_indicadores
        return render(request,'Instrumento/Observacion/obs_editar.html', { 
            'instrumento':the_obs, 
            'indicadores' : the_indicadores, 
            "ind_choices" : IndicadorListaObs.TIPO_CHOICES,
            "ASIGNATURAS" : Asignatura.objects.all(),
        })

    return render(request,'Instrumento/Observacion/obs_editar.html', {
        "ind_choices" : IndicadorListaObs.TIPO_CHOICES,
        "ASIGNATURAS" : Asignatura.objects.all(),
    })
