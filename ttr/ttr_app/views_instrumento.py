# -*- coding: utf-8 -*-
from django.db import IntegrityError
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from ttr_app.models import *
import json
from django.http import HttpResponse, HttpResponseRedirect

def instrumento(request):
    url_redirect = '/'
    if (request.method == "GET"):
        idx = request.GET.get('id')
        edit = request.GET.get('edit')
        oficial = request.GET.get('oficial')
        inst = get_object_or_404(InstrumentoEvaluacion, pk=int(idx))
        print (inst)
        if oficial:
            inst.oficial = (oficial.lower()=='true')
            inst.save()
            res = {
                "result" : "true",
                "oficial" : inst.oficial,
            }
            return HttpResponse(json.dumps(res), mimetype='application/json')
        try:
            if inst.rubrica:
                url_redirect = ('/instrumento/rubrica/editar/?id='+idx) if (edit=='true') else ('/instrumento/rubrica/ver/?id='+idx)
        except:
            pass
        try:
            if inst.listacotejo:
                url_redirect = ('/instrumento/listacotejo/editar/?id='+idx) if (edit=='true') else ('/instrumento/listacotejo/ver/?id='+idx)
        except:
            pass
        try:
            if inst.listaobservacion :
                url_redirect = ('/instrumento/listaobs/editar/?id=' + idx) if ('/instrumento/listacotejo/ver/?id='+idx) else ('/instrumento/listaobs/ver/?id=' + idx)
        except:
            pass
        
    return HttpResponseRedirect(url_redirect)

def rating(request):
    url_redirect = '/'
    if (request.method == "POST"):
        idx = request.GET.get('id')
        rating = request.POST.get('rating')
        inst = get_object_or_404(InstrumentoEvaluacion, pk=int(idx))
        evaluacion = EvaluacionInstrumento(
            user_id=request.user.pk,
            instrumento_id=inst.pk,
            valor=rating,
        )
        evaluacion.save()
        return HttpResponse('true')
        
    return HttpResponse('false')

def eliminar(request):
    url_redirect = '/'
    if (request.method == "POST"):
        idx = request.GET.get('id')
        inst = get_object_or_404(InstrumentoEvaluacion, pk=int(idx))
        print (inst)
        inst.delete()
        return HttpResponse('false')
        
    return HttpResponse('false')
