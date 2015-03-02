# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import math

class Plantel(models.Model):
	nombre = models.CharField(max_length=60, null=True, blank=True)
	url_logo = models.CharField(max_length=65535, null=True, blank=True)
	mision = models.CharField(max_length=65535, null=True, blank=True)
	vision = models.CharField(max_length=65535, null=True, blank=True)
	# usuarios = models.ManyToManyField(MyUser)

	MEDIA_SUP = 1
	SUPERIOR = 2
	NIVEL_CHOICES = (
		(MEDIA_SUP, "Media Superior"),
		(SUPERIOR, "Superior"),
	)
	nivel = models.IntegerField(choices=NIVEL_CHOICES, default=SUPERIOR)

	def __unicode__(self):              # __unicode__ on Python 2
		return self.nombre or ''

class MyUser(User):
	"""
	Modelo personalizado de usuarios
	"""
	full_name = models.CharField(max_length=60, null=True, blank=True)
	# SUPER_ADMIN = 1
	ADMINISTRADOR = 2
	PROFESOR = 3
	TIPO_CHOICES = (
		(ADMINISTRADOR, "Administrador"),
		(PROFESOR, "Profesor"),
		# (SUPER_ADMIN, "Super Administrador"),
	)
	rol = models.IntegerField(choices=TIPO_CHOICES, default=PROFESOR)
	plantel = models.ForeignKey(Plantel)

	def __unicode__(self):              # __unicode__ on Python 2
		return self.get_full_name()

	def save(self, *args, **kwargs):
		if self.pk is None:
			self.set_password(self.password)
		self.full_name = self.get_full_name()
		super(MyUser, self).save(*args, **kwargs)

class Departamento(models.Model):
	nombre = models.CharField(max_length=60, null=True, blank=True)
	plantel = models.ForeignKey(Plantel)

	def __unicode__(self):              # __unicode__ on Python 2
		return self.nombre or ''

class Academia(models.Model):
	nombre = models.CharField(max_length=60, null=True, blank=True)
	depto = models.ForeignKey(Departamento)

	def __unicode__(self):              # __unicode__ on Python 2
		return self.nombre

class Asignatura(models.Model):
	nombre = models.CharField(max_length=60, null=True, blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	autor = models.ForeignKey(MyUser, related_name="asignatura_autor")
	academia = models.ForeignKey(Academia)
	presidente = models.ForeignKey(MyUser, related_name="asignatura_presidente", null=True, blank=True)

	def __unicode__(self):              # __unicode__ on Python 2
		return self.nombre

class Clases (models.Model):
	asignaturas = models.ManyToManyField(Asignatura null=True, blank=True)
	user = models.OneToOneField(MyUser, primary_key=True)

#####################
class InstrumentoEvaluacion(models.Model):
	GENERAL = 0
	PLANTEL = 1
	TIPO_CHOICES = (
		(GENERAL, "General"),
		(PLANTEL, "Plantel"),
	)
	level_show = models.IntegerField(choices=TIPO_CHOICES, default=PLANTEL)

	titulo = models.CharField(max_length=60, null=True, blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	autor = models.ForeignKey(MyUser, related_name="instrumento_autor")
	asignatura = models.ForeignKey(Asignatura, null=True, blank=True)
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
	rubrica = models.ForeignKey(Rubrica)

	def __unicode__(self):              # __unicode__ on Python 2
		return str(self.valor)

class CriterioRubrica (models.Model):
	rubrica = models.ForeignKey(Rubrica)
	ponderacion = models.ForeignKey(PonderacionRubrica)
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
	check = models.BooleanField(default=False) #definir valor maximo y minimo #valor hecho, no realizado, pendiente

	def __unicode__(self):              # __unicode__ on Python 2
		return self.texto

#####################
class ListaObservacion(InstrumentoEvaluacion):
	pass

class IndicadorListaObs(models.Model):
	listaobs = models.ForeignKey(ListaObservacion)
	texto = models.CharField(max_length=60, null=True, blank=True)

	SIN_VALOR 	= 0
	MUY_MALO 	= 1
	MALO 		= 2
	REGULAR 	= 3
	BUENO 		= 4
	EXCELENTE 	= 5
	TIPO_CHOICES = (
		(SIN_VALOR, "Sin valorar"),
		(MUY_MALO, "Muy malo"),
		(MALO, "Malo"),
		(REGULAR, "Regular"),
		(BUENO, "Bueno"),
		(EXCELENTE, "Excelente"),
	)
	valor = models.IntegerField(choices=TIPO_CHOICES, default=SIN_VALOR) 

	def __unicode__(self):              # __unicode__ on Python 2
		return self.texto

#####################
class EvaluacionInstrumento(models.Model):
	user = models.ForeignKey(MyUser)
	instrumento = models.ForeignKey(InstrumentoEvaluacion)
	valor = models.IntegerField() #definir valor maximo y minimo

	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_modif = models.DateTimeField(auto_now=True)

class ComentarioInstrumento(models.Model):
	user = models.ForeignKey(MyUser)
	instrumento = models.ForeignKey(InstrumentoEvaluacion)
	texto = models.CharField(max_length=65535, null=True, blank=True)
	
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_modif = models.DateTimeField(auto_now=True)
