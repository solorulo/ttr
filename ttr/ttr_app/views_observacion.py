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

def agregar(request):
    if request.method == "POST":
        titulo = request.POST.get('titulo')
        autor = request.POST.get('autor')
        asignatura = request.POST.get('asignatura')
        oficial = request.POST.get('oficial')

        print request.POST

        listaobs = request.POST.get('listaobs[]')
        print "listaobs "
        print listaobs
        listaobs = json.loads(listaobs)

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
        {"ind_choices" : IndicadorListaObs.TIPO_CHOICES })

def ver(request):
    idx = request.GET.get('id')
    the_obs = ListaObservacion.objects.get(pk=int(idx))
    the_indicadores = IndicadorListaObs.objects.filter(listaobs_id=the_obs.pk)
    print the_indicadores
    return render(request,'Instrumento/Observacion/obs_ver.html', 
        { 'instrumento':the_obs, 'indicadores' : the_indicadores })
