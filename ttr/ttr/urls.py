# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ttr.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^index/', 'ttr_app.views.index'),
    url(r'^login/', 'ttr_app.views.login'),

    url(r'^estructura/$', 'ttr_app.views.estructura'),

    url(r'^estructura/json/(?P<node>\w+)(/(?P<node_id>\d{1,5}))?$', 'ttr_app.views.estructura_json'),

    url(r'^estructura/json/$', 'ttr_app.views.estructura_json'),



    url(r'^asignatura/$','ttr_app.views.newAsignature'),
    url(r'^asignatura/agregar$','ttr_app.views.registrarAsignatura'),                       
    url(r'^asignatura/ver$','ttr_app.views.verAsignaturas'),
    url(r'^asignatura/delete$','ttr_app.views.eliminarAsignatura'),
    url(r'^asignatura/consultar/$','ttr_app.views.consultarAsignatura'),
    url(r'^asignatura/consultar/modificar','ttr_app.views.editarAsignatura'),


    url(r'^area/nueva$','ttr_app.views.newArea'),
    url(r'^area/ver$','ttr_app.views.verAreas'),
    url(r'^area/delete$','ttr_app.views.eliminarArea'),
    url(r'^area/consultar/$','ttr_app.views.consultarArea'),
    url(r'^area/consultar/modificar','ttr_app.views.editarArea'),


    url(r'^departamento/nuevo$','ttr_app.views.newDepto'),
    url(r'^departamento/agregar$','ttr_app.views.registrarDepto'),
    url(r'^departamento/ver$','ttr_app.views.verDeptos'),
    url(r'^departamento/delete$','ttr_app.views.eliminarDepto'),
    url(r'^departamento/consultar/$','ttr_app.views.consultarDepto'),
    url(r'^departamento/consultar/modificar','ttr_app.views.editarDepto'),
    # url(r'^instrumentos/', ''),
    # url(r'^instrumento/', ''),
    # url(r'^instrumento/agregar', ''),
    url(r'^instrumento/rubrica/agregar', 'ttr_app.views_rubrica.agregar'),
    # url(r'^instrumento/listacotejo/agregar', ''),
    # url(r'^instrumento/listaobservacion/agregar', ''),
    # url(r'^instrumento/borrar', ''),
    # url(r'^login/', ''),
    url(r'^usuarios/', 'ttr_app.views.visualizarUsuario'),
    url(r'^usuario/$', 'ttr_app.views.newUser'),
    url(r'^usuario/agregar/$', 'ttr_app.views.registrarUsuario'),
    url(r'^usuario/borrar/', 'ttr_app.views.eliminarUsuario'),
    url(r'^usuario/consultar/$','ttr_app.views.consultarUsuario'),
    url(r'^usuario/consultar/modificar','ttr_app.views.editarUsuario')
    # url(r'^areas/', ''),
    # url(r'^area/', ''),
    # url(r'^area/agregar', ''),
    # url(r'^area/borrar', ''),
    # url(r'^departamentos/', ''),
    # url(r'^departamento/', ''),
    # url(r'^departamento/agregar', ''),
    # url(r'^departamento/borrar', ''),
    # url(r'^asignaturas/', ''),
    # url(r'^asignatura/', ''),
    # url(r'^asignatura/agregar', ''),
    # url(r'^asignatura/borrar', ''),
)
