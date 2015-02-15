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

        new_rubrica = Rubrica(
            titulo=titulo,
            autor_id=int(autor),
            asignatura_id=int(asignatura),
            oficial=(oficial=="true"),
        )
        new_rubrica.save()

        categorias = {}
        ponderacion_vals = {}
        for idx1, cat in enumerate(cats):
            print ("nueva cat")
            print cat
            """
            'val' : cat,
            'index_cat' : meta_index_cat
            """
            cat_val = cat['val']
            cat_index = cat['index_cat']
            new_cat = CategoriaRubrica(
                texto=cat_val,
                rubrica_id=new_rubrica.pk
            )
            new_cat.save()
            categorias[idx1] = new_cat

        for idx, pod_val in enumerate(pod_vals):
            print ("nueva pond_val")
            print pod_val
            """
            'index_pod' : meta_index,
            'meta_new' : meta_new,
            'text' : input_text
            """
            # index_pod = pod_val['index_pod']
            pod_text = pod_val['text']

            new_pond_val = PonderacionRubrica(
                rubrica_id=new_rubrica.pk,
                valor=pod_text
            )
            new_pond_val.save() 
            ponderacion_vals[idx] = new_pond_val

        for idx, pod in enumerate(pods):
            print ("nueva pond")
            print pod
            """
            'index' : indexPond,
            'cat' : indexRow,
            'val' : val
            """
            index_cat = pod['cat']
            pod_val = pod['val']
            indexPond = pod['index']

            new_pond = CriterioRubrica(
                rubrica_id=new_rubrica.pk,
                ponderacion_id=ponderacion_vals[indexPond].pk,
                categoria_id=categorias[index_cat].pk,
                descripcion=pod_val)
            new_pond.save() 
        return HttpResponse('true')
    return render(request,'Instrumento/Rubrica/rubrica_agregar.html')

def ver(request):
    idx = request.GET.get('id')
    the_rubrica = Rubrica.objects.get(pk=int(idx))
    the_cats = CategoriaRubrica.objects.filter(rubrica_id=the_rubrica.pk)
    the_ponds = PonderacionRubrica.objects.filter(rubrica_id=the_rubrica.pk)
    fpods = CriterioRubrica.objects.filter(rubrica_id=the_rubrica.pk)
    print the_rubrica
    print the_cats
    print the_ponds
    print fpods
    return render(request,'Instrumento/Rubrica/rubrica_ver.html', 
        { 'rubrica':the_rubrica, 'cats' : the_cats, 'pods' : fpods, 'pod_vals' : the_ponds })
