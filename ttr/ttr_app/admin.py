# -*- coding: utf-8 -*-
from ttr_app.models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
#from django.contrib.auth.models import User #, Group

"""
Aquí agregamos los modelos que se muestran en el administrador de Django (/admin).
"""
admin.site.register(MyUser)

# Register your models here.
admin.site.register(Departamento)
admin.site.register(Plantel)
admin.site.register(Academia)
admin.site.register(Asignatura)
admin.site.register(Clases)
admin.site.register(InstrumentoEvaluacion)
admin.site.register(Rubrica)
admin.site.register(CategoriaRubrica)
admin.site.register(PonderacionRubrica)
admin.site.register(ListaCotejo)
admin.site.register(IndicadorCotejo)
admin.site.register(ListaObservacion)
# admin.site.register(CategoriaListaObs)
admin.site.register(IndicadorListaObs)
admin.site.register(EvaluacionInstrumento)
admin.site.register(ComentarioInstrumento)
