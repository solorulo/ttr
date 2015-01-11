# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import math

"""
Modelo personalizado de usuario que permite campos mas grandes
"""
class MyUser(User):
	ADMINISTRADOR = 0
	PROFESOR = 1
	TIPO_CHOICES = (
		(ADMINISTRADOR, "Administrador"),
		(PROFESOR, "Profesor"),
	)
	rol = models.IntegerField(choices=TIPO_CHOICES, default=PROFESOR)

	def __unicode__(self):              # __unicode__ on Python 2
		return self.get_full_name()

	def save(self, *args, **kwargs):
		if self.pk is None:
			self.set_password(self.password)
		super(MyUser, self).save(*args, **kwargs)

class Area(models.Model):
	nombre = models.CharField(max_length=60, null=True, blank=True)

	def __unicode__(self):              # __unicode__ on Python 2
		return self.nombre or ''

class Departamento(models.Model):
	nombre = models.CharField(max_length=60, null=True, blank=True)
	area = models.ForeignKey(Area)

	def __unicode__(self):              # __unicode__ on Python 2
		return self.nombre

class Asignatura(models.Model):
	nombre = models.CharField(max_length=60, null=True, blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	autor = models.ForeignKey(MyUser, related_name="asignatura_autor")
	departamento = models.ForeignKey(Departamento)
	presidente = models.ForeignKey(MyUser, related_name="asignatura_presidente")

	def __unicode__(self):              # __unicode__ on Python 2
		return self.nombre

class Clases (models.Model):
	asignaturas = models.ManyToManyField(Asignatura)
	user = models.OneToOneField(MyUser, primary_key=True)

#####################
class InstrumentoEvaluacion(models.Model):
	titulo = models.CharField(max_length=60, null=True, blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	autor = models.ForeignKey(MyUser, related_name="instrumento_autor")
	asignatura = models.ForeignKey(Asignatura)
	oficial = models.BooleanField(default=False)
	fecha_modif = models.DateTimeField(auto_now=True)

	def __unicode__(self):              # __unicode__ on Python 2
		return self.titulo

#####################
class Rubrica (InstrumentoEvaluacion):
	pass

class CategoriaRubrica (models.Model):
	texto = models.CharField(max_length=60, null=True, blank=True)
	rubrica = models.ForeignKey(Rubrica)

	def __unicode__(self):              # __unicode__ on Python 2
		return self.texto

class PonderacionRubrica (models.Model):
	valor = models.IntegerField()
	categoria = models.ForeignKey(CategoriaRubrica)
	descripcion = models.CharField(max_length=60, null=True, blank=True)

	def __unicode__(self):              # __unicode__ on Python 2
		return self.descripcion

#####################
class ListaCotejo (InstrumentoEvaluacion):
	pass

class IndicadorCotejo(models.Model):
	listacotejo = models.ForeignKey(ListaCotejo)
	texto = models.CharField(max_length=60, null=True, blank=True)
	valor= models.IntegerField() #definir valor maximo y minimo #valor hecho, no realizado, pendiente

	def __unicode__(self):              # __unicode__ on Python 2
		return self.texto

#####################
class ListaObservacion(InstrumentoEvaluacion):
	pass

class CategoriaListaObs(models.Model):
	listaobs = models.ForeignKey(ListaObservacion)
	texto = models.CharField(max_length=60, null=True, blank=True)

	def __unicode__(self):              # __unicode__ on Python 2
		return self.texto

class IndicadorListaObs(models.Model):
	categoriaobs = models.ForeignKey(CategoriaListaObs)
	texto = models.CharField(max_length=60, null=True, blank=True)
	valor = models.IntegerField() 

	def __unicode__(self):              # __unicode__ on Python 2
		return self.texto

#####################
class EvaluacionInstrumento(models.Model):
	user = models.ForeignKey(MyUser)
	instrumento = models.ForeignKey(InstrumentoEvaluacion)
	valor = models.IntegerField() #definir valor maximo y minimo
