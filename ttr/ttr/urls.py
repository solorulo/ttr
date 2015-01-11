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
    # url(r'^instrumentos/', ''),
    # url(r'^instrumento/', ''),
    # url(r'^instrumento/agregar', ''),
    # url(r'^instrumento/rubrica/agregar', ''),
    # url(r'^instrumento/listacotejo/agregar', ''),
    # url(r'^instrumento/listaobservacion/agregar', ''),
    # url(r'^instrumento/borrar', ''),
    # url(r'^login/', ''),
    # url(r'^usuarios/', ''),
    url(r'^usuario/$', 'ttr_app.views.newUser'),
    url(r'^usuario/agregar/$', 'ttr_app.views.registrarUsuario'),
    # url(r'^usuario/borrar', ''),
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
