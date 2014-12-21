# -*- coding: utf-8 -*-
from django.db import IntegrityError
from django.shortcuts import render

# Create your views here.
def estructura(request):
	return render(request, 'estructura.html')