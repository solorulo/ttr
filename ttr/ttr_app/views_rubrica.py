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
        print request.POST
        pod_vals = request.POST.get('pod_vals[]')
        print "pod_vals "
        print pod_vals
        pod_vals = json.loads(pod_vals)
        cats = request.POST.get('cats[]')
        print "cats "
        print cats
        cats = json.loads(cats)
        pods = request.POST.get('pods[]')
        print "pods "
        print pods
        pods = json.loads(pods)
        titulo = request.POST.get('titulo')
        autor = request.POST.get('autor')
        asignatura = request.POST.get('asignatura')
        oficial = request.POST.get('oficial')

        new_rubrica = Rubrica(
            titulo=titulo,
            autor_id=autor,
            asignatura_id=asignatura,
            oficial=(oficial=="true"),
        )
        new_rubrica.save()

        categorias = {}
        for idx1, cat in enumerate(cats):
            print ("nueva cat")
            print cat
            cat_val = cat['val']
            cat_index = cat['index_cat']
            new_cat = CategoriaRubrica(
                texto=cat_val,
                rubrica_id=new_rubrica.pk
            )
            new_cat.save()
            categorias[idx1] = new_cat

        for idx, pod in enumerate(pods):
            print ("nueva pond")
            print pod
            index_cat = pod['cat']
            pod_val = pod['val']

            new_pond = PonderacionRubrica(
                valor=int(pod_vals[idx]['text']),
                categoria=categorias[index_cat],
                descripcion=pod_val)
            new_pond.save()
        return HttpResponse('true')
    return render(request,'rubrica_agregar.html')
