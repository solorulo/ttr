# -*- coding: utf-8 -*-
from django.db import IntegrityError
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from ttr_app.models import *
import json
from django.http import HttpResponse, HttpResponseRedirect

def instrumento(request):
    url_redirect = '/'
    if (request.method == "GET"):
        idx = request.GET.get('id')
        oficial = request.GET.get('oficial')
        inst = InstrumentoEvaluacion.objects.get(pk=int(idx))
        print inst
        if oficial:
            inst.oficial = (oficial.lower()=='true')
            inst.save()
            res = {
                "result" : "true",
                "oficial" : inst.oficial,
            }
            return HttpResponse(json.dumps(res), mimetype='application/json')
        if inst.rubrica:
            url_redirect = '/instrumento/rubrica/ver/?id='+idx
        elif inst.listacotejo:
            url_redirect = '/instrumento/listacotejo/ver/?id='+idx
        elif inst.listaobservacion :
            url_redirect = '/instrumento/listaobs/ver/?id=' + idx
    return HttpResponseRedirect(url_redirect)
