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

        print (request.POST)

        try:
            autor = request.user.myuser.pk
        except:
            pass

        listacotejo = request.POST.get('listacotejo[]')
        print ("listacotejo ")
        print (listacotejo)
        listacotejo = json.loads(listacotejo)

        new_listacotejo = ListaCotejo(
            titulo=titulo,
            autor_id=int(autor),
            asignatura_id=int(asignatura),
            oficial=(oficial.lower()=="true"),
        )
        new_listacotejo.save()

        for idx, indicador in enumerate(listacotejo):
            print ("nuevo indicador")
            print (indicador)
            """
            'text' : text,
            'checked' : checked,
            'index' : meta_index
            """
            ind_text = indicador['text']
            ind_checked = indicador['checked']
            observ = indicador['observ']
            new_indicador = IndicadorCotejo(
                listacotejo_id=new_listacotejo.pk,
                texto=ind_text,
                check=ind_checked,
                observaciones=observ,
            )
            new_indicador.save()
        
        return HttpResponse('true')
    return render(request,'Instrumento/Cotejo/cotejo_agregar.html',
        { "ASIGNATURAS" : Asignatura.objects.all(), })

def ver(request):
    idx = request.GET.get('id')
    the_cotejo = ListaCotejo.objects.get(pk=int(idx))
    the_indicadores = IndicadorCotejo.objects.filter(listacotejo_id=the_cotejo.pk)
    print (the_indicadores)
    return render(request,'Instrumento/Cotejo/cotejo_ver.html', 
        { 'instrumento':the_cotejo, 'indicadores' : the_indicadores })


def editar(request):
    idx = request.GET.get('id')
    if request.method == "POST":
        titulo = request.POST.get('titulo')
        autor = request.POST.get('autor')
        asignatura = request.POST.get('asignatura')
        oficial = request.POST.get('oficial')

        print (request.POST)

        listacotejo = request.POST.get('listacotejo[]')
        print ("listacotejo ")
        print (listacotejo)
        listacotejo = json.loads(listacotejo)

        try:
            autor = request.user.myuser.pk
            new_listacotejo = get_object_or_404(ListaCotejo,
                pk=int(idx),
                autor_id=autor,
            )
        except:
            pass

        new_listacotejo.titulo=titulo
        new_listacotejo.autor_id=int(autor)
        new_listacotejo.asignatura_id=int(asignatura)
        new_listacotejo.oficial=(oficial.lower()=="true")
        new_listacotejo.save()

        IndicadorCotejo.objects.filter(listacotejo_id=new_listacotejo.pk).delete()
        for idx, indicador in enumerate(listacotejo):
            print ("nuevo indicador")
            print (indicador)
            """
            'text' : text,
            'checked' : checked,
            'index' : meta_index
            """
            ind_text = indicador['text']
            ind_checked = indicador['checked']
            observ = indicador['observ']
            new_indicador = IndicadorCotejo(
                listacotejo_id=new_listacotejo.pk,
                texto=ind_text,
                check=ind_checked,
                observaciones=observ,
            )
            new_indicador.save()
        
        return HttpResponse('true')
    elif request.method == "GET":
        the_cotejo = get_object_or_404(ListaCotejo, pk=int(idx))
        the_indicadores = IndicadorCotejo.objects.filter(listacotejo_id=the_cotejo.pk)
        print (the_indicadores)
        return render(request,'Instrumento/Cotejo/cotejo_editar.html', { 
            'instrumento':the_cotejo, 
            'indicadores' : the_indicadores,
            "ASIGNATURAS" : Asignatura.objects.all(),
         })
    return render(request,'Instrumento/Cotejo/cotejo_editar.html',
        { "ASIGNATURAS" : Asignatura.objects.all(), })
