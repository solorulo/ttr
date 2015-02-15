# -*- coding: utf-8 -*-
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from ttr_app.models import *
import json
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect

def comment (request):
    if request.method == 'POST':
        idx = request.POST.get('id')
        comment = request.POST.get('text')
        user_id = request.POST.get('user_id', request.user.pk)
        the_inst = InstrumentoEvaluacion.objects.get(pk=int(idx))
        new_comment = ComentarioInstrumento(
            user_id=int(user_id),
            instrumento_id=the_inst.pk,
            texto=comment,
        )
        new_comment.save()
        return HttpResponse('true')

    idx = request.GET.get('id')
    the_comment = ComentarioInstrumento.objects.get(pk=idx).values()
    return HttpResponse(json.dumps(the_comment), mimetype='application/json') 

def get_comments(request):
    idx = request.GET.get('id')
    the_cinsts = ComentarioInstrumento.objects
        .filter(instrumento_id=int(idx))
        .order_by('-fecha_creacion')
        .select_related()
    res = []
    for cint in the_cinsts:
        res.append({
            'pk' : cint.pk,
            'texto' : cint.texto,
            'user' : {
                'pk' : cint.user.pk,
                'full_name' : cint.user.get_full_name(),
            }
        }) 

    return HttpResponse(json.dumps(res), mimetype='application/json')
