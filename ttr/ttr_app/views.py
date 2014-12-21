# -*- coding: utf-8 -*-
from django.db import IntegrityError
from django.shortcuts import render

# Create your views here.
def estructura(request):
	return render(request, 'estructura.html')
def login(request):
    return render(request, 'login.html')
def index(request):
    return render(request, 'index.html')